from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
import datetime
import copy

from kivymd.app import MDApp

from data.database import insert_data
from data.engine.constants import NOTATION_TO_POS_HINT, NOTATION_TO_GAME_STATE, GAME_STATE_TO_NOTATION, columns, rows, RANKS, FILES, GAME_STATE_TO_NOTATION_FLIPPED, NOTATION_TO_POS_HINT_FLIPPED
from data.engine.engine import Game
from data.engine.evaluate import score
from data.engine.search import random_move_search, search
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import get_color_from_hex
from data import settings
from kivy.core.audio import SoundLoader


class Piece(Image):
    def __init__(self, piece_position, piece_name, flipped=False, **kwargs):
        super(Piece, self).__init__(**kwargs)
        self.name = piece_name
        self.position = piece_position
        self.size_hint = (.125, .125)
        self.pos_hint = {'x': NOTATION_TO_POS_HINT[piece_position][0], 'y': NOTATION_TO_POS_HINT[piece_position][1]}
        if flipped:
            self.pos_hint = {'x': NOTATION_TO_POS_HINT_FLIPPED[piece_position][0], 'y': NOTATION_TO_POS_HINT_FLIPPED[piece_position][1]}
        self.source = "data/img/" + self.name + ".png"
        self.fit_mode = "fill"


class Mark(MDLabel):
    light_color = (1, 1, 1, 1)
    dark_color = (0.467, 0.58, 0.333, 1)

    def __init__(self, position, color="light", flipped=False, **kwargs):
        super(Mark, self).__init__(**kwargs)
        self.dark_color = get_color_from_hex(settings.dark_square_color) if settings.dark_square_color else self.dark_color
        self.text = ""
        self.font_size = 16
        self.bold = True
        self.halign = 'right'
        self.size_hint = (.0625, .0625)
        self.pos_hint = {'x': NOTATION_TO_POS_HINT[position][0] + .0625,
                         'y': NOTATION_TO_POS_HINT[position][1] - .015625}
        self.color = self.dark_color if color == "light" else self.light_color
        if position[1] == '1':
            self.text = position[0] if not flipped else FILES[position[0]]
        if position[0] == 'a' and position[1] != '1':
            self.text = position[1] if not flipped else RANKS[position[1]]
            self.halign = 'left'
            self.pos_hint = {'x': NOTATION_TO_POS_HINT[position][0], 'y': NOTATION_TO_POS_HINT[position][1] + 0.078125}



class Square(Image):
    light_color = (1, 1, 1, 1)
    dark_color = (0.467, 0.58, 0.333, 1)

    def __init__(self, position, color="light", **kwargs):
        super(Square, self).__init__(**kwargs)
        self.dark_color = get_color_from_hex(settings.dark_square_color) if settings.dark_square_color else self.dark_color
        self.size_hint = (.125, .125)
        self.pos_hint = {'x': NOTATION_TO_POS_HINT[position][0], 'y': NOTATION_TO_POS_HINT[position][1]}
        self.color = self.light_color if color == "light" else self.dark_color


class Highlight(Image):
    def __init__(self, position, **kwargs):
        super(Highlight, self).__init__(**kwargs)
        self.size_hint = (.0625, .0625)
        self.pos_hint = {'x': NOTATION_TO_POS_HINT[position][0] + .03125, 'y': NOTATION_TO_POS_HINT[position][1] + .03125}
        self.notation = position
        self.toggle = False
        self.color = (1, 0, 0, 0)


def normal_move_sound():
    if settings.sounds:
        sound = SoundLoader.load("data/audio/StandardMove.mp3")
        if sound:
            sound.play()


def capture_move_sound():
    if settings.sounds:
        sound = SoundLoader.load("data/audio/CaptureMove.mp3")
        if sound:
            sound.play()


def duck_move_sound():
    if settings.sounds:
        sound = SoundLoader.load("data/audio/DuckMove.mp3")
        if sound:
            sound.play()


class Board(FloatLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.notation_box_move_black = None
        self.notation_box_move_white = None
        self.notation_box_move_count = None
        self.dialog = None
        self.duck = None
        self.is_duck_on_board = None
        self.next_player_turn = None
        self.square_from = None
        self.selected_piece = None
        self.marking = None
        self.pieces = None
        self.legal_duck_moves = None
        self.legal_moves = None
        self.game = None
        self.highlight_on = None
        self.player_id = None
        self.highlights = None
        self.is_black_engine = None
        self.is_white_engine = None
        self.notation_box = None
        self.notation_count = None
        self.dialog_showed = None
        self.bot_duck_move = None
        self.player_side = None

    def initialize_board(self):
        Window.bind(on_key_down=self.key_action)
        self.game = Game()
        self.legal_moves = self.game.generate_pseudo_legal_moves()
        self.legal_duck_moves = None
        self.dialog = None
        self.duck = None
        self.square_from = None
        self.selected_piece = None
        self.pieces = {}
        self.marking = {}
        self.highlights = {}
        self.player_id = settings.logged_id
        self.next_player_turn = True
        self.is_duck_on_board = False
        self.highlight_on = True if settings.highlights else False
        self.notation_count = 0
        self.notation_box = None
        self.dialog_showed = False
        self.set_board()

    def unbind_keys(self):
        Window.unbind(mouse_pos=self.mouse_off_board)
        pass

    def mouse_off_board(self, window, pos):
        bounds = self.get_board_bound()
        if (pos[0] < bounds[0] or pos[0] > bounds[2] or pos[1] < bounds[1] or pos[1] > bounds[3]) and self.selected_piece is not None:
            self.deselect_piece()

    def set_board(self):
        for row_index, row in enumerate(self.game.state):
            for col_index, col in enumerate(row):
                notation = GAME_STATE_TO_NOTATION[(row_index, col_index)]
                square = Square(notation, "dark")
                if (row_index + col_index) % 2 != 1:
                    square = Square(notation)
                highlight = Highlight(notation)
                self.highlights[notation] = highlight
                self.add_widget(square)
                self.add_widget(highlight)
        self.set_marking()
        self.set_pieces()

    def set_marking(self):
        for row_index, row in enumerate(self.game.state):
            for col_index, col in enumerate(row):
                notation = GAME_STATE_TO_NOTATION[(row_index, col_index)]
                mark = Mark(notation, "dark", self.game.flipped)
                if (row_index + col_index) % 2 != 1:
                    mark = Mark(notation, flipped=self.game.flipped)
                self.add_widget(mark)
                self.marking[notation] = mark
                if notation == 'a1':
                    mark = Mark(notation, flipped=self.game.flipped)
                    mark.text = '1' if not self.game.flipped else '8'
                    mark.color = mark.light_color
                    mark.halign = 'left'
                    mark.pos_hint = {'x': NOTATION_TO_POS_HINT[notation][0], 'y': NOTATION_TO_POS_HINT[notation][1] + 0.078125}
                    self.add_widget(mark)
                    self.marking[notation + "_"] = mark

    def set_pieces(self):
        for row_index, row in enumerate(self.game.state):
            for col_index, col in enumerate(row):
                if col != "--":
                    if self.game.flipped:
                        notation = GAME_STATE_TO_NOTATION_FLIPPED[(row_index, col_index)]
                    else:
                        notation = GAME_STATE_TO_NOTATION[(row_index, col_index)]
                    piece = Piece(notation, col, flipped=self.game.flipped)
                    if col == "DD":
                        self.duck = piece
                    self.pieces[notation] = piece
                    self.add_widget(piece)

    def clear_board(self):
        for piece in self.pieces:
            self.remove_widget(self.pieces[piece])
        self.pieces = {}
        for square in self.highlights.values():
            square.color = (1, 0, 0, 0)

    def key_action(self, *args):
        key_pressed = list(args)
        if self.parent.parent.parent:
            if key_pressed[-3] == 80:
                self.game.prev_move()
                self.update_board()
            if key_pressed[-3] == 79:
                self.game.next_move()
                self.update_board()
            if key_pressed[-3] == 81:
                self.game.prev_last()
                self.update_board()
            if key_pressed[-3] == 82:
                self.game.next_last()
                self.update_board()

    def show_score(self, dt):
        print(score(self.game.state))

    def bot_first_move(self):
        move = random_move_search(self.legal_moves)
        self.bot_move(move)
        if not self.game.end:
            move = random_move_search(self.legal_duck_moves)
            self.duck_bot_move(move)

    def bot_move(self, move):
        self.game.make_move(move)
        self.update_board()
        self.next_player_turn = False
        self.legal_duck_moves = self.game.generate_duck_moves()

    def duck_bot_move(self, move):
        if not self.game.duck_moves:
            self.game.duck_place(move.end)
            self.update_board()
            self.is_duck_on_board = True
            self.next_player_turn = True
            self.legal_moves = self.game.generate_pseudo_legal_moves()
        else:
            self.game.duck_move(move)
            self.update_board()
            self.next_player_turn = True
            self.legal_moves = self.game.generate_pseudo_legal_moves()

    def call_unmake_move(self):
        if self.game.moves_point is None or (self.game.moves_point is not None and self.game.moves_point == len(self.game.moves) - 1):
            self.next_player_turn = self.next_player_turn if len(self.game.moves) == len(
                self.game.duck_moves) else not self.next_player_turn
            if self.game.end:
                self.game.end = False
            self.game.unmake_move()
            self.update_board()
            self.is_duck_on_board = False if not self.game.duck_moves else True
            if self.game.moves:
                self.game.en_passant_rights(self.game.moves[-1])
            self.legal_moves = self.game.generate_pseudo_legal_moves()

    def update_board(self):
        self.clear_board()
        self.set_pieces()
        self.show_dialog()

    def update_board_hard(self):
        self.clear_board()
        for mark in self.marking:
            self.remove_widget(self.marking[mark])
        self.set_marking()
        self.set_pieces()
        self.show_dialog()

    def get_board_bound(self):
        return self.pos[0], self.pos[1], self.pos[0] + self.size[0], self.pos[1] + self.size[1]

    def show_dialog(self):
        if self.game.end and not self.dialog_showed:
            who_wins = "Wygrał "
            who_wins += "Biały" if self.game.whoToMove == 1 else "Czarny"
            result = "1-0" if self.game.whoToMove == 1 else "0-1"
            player = "BOT" if self.is_black_engine == 1 or self.is_white_engine == 1 else "Inny gracz"
            time = str(datetime.datetime.now())
            if not self.dialog:
                self.dialog = MDDialog(
                    title=who_wins,
                    text=f"{result} przeciwko {player}, partia zajeła {self.notation_count} ruchów, {time[:-7]}",
                )

            if settings.logged == "gracz":
                insert_data("INSERT INTO chessgames VALUES (NULL, ?, ?, ?, ?, ?, ?)", (self.player_id, player, self.player_side, result, self.notation_count, time))

            self.dialog.open()
            self.dialog_showed = True

    def on_touch_down(self, touch):
        x_min, y_min, x_max, y_max = self.get_board_bound()
        if ((touch.pos[0] < x_min or touch.pos[0] > x_max or touch.pos[1] < y_min or touch.pos[1] > y_max) and
                self.selected_piece is not None):
            self.deselect_piece()
        bound = {(x_min + j * x_min, y_min + i * y_min): columns[j] + rows[i]
                 for i in range(len(rows)) for j in range(len(columns))}
        for pos, clicked_square in bound.items():
            if ((pos[0] < touch.pos[0] < pos[0] + x_min and pos[1] < touch.pos[1] < pos[1] + y_min) and
                    (x_min < touch.pos[0] < x_max and y_min < touch.pos[1] < y_max)):
                if self.next_player_turn:
                    if self.selected_piece is None:
                        possible_to_select = {key: value for key, value in self.pieces.items()
                                              if (value.name[1] == 'B' and self.game.whoToMove == -1 and self.is_black_engine == -1)
                                              or value.name[1] == 'W' and self.game.whoToMove == 1 and self.is_white_engine == -1}
                        if clicked_square in possible_to_select and self.game.moves_point is None:
                            if self.game.moves_point is None:
                                self.select_piece(clicked_square)
                    elif self.selected_piece:
                        self.execute_move(self.square_from, clicked_square)
                elif not self.next_player_turn:
                    if not self.is_duck_on_board:
                        if self.game.state[NOTATION_TO_GAME_STATE[clicked_square][0]][NOTATION_TO_GAME_STATE[clicked_square][1]] == '--':
                            self.place_duck(clicked_square)
                            self.is_duck_on_board = True
                            self.next_player_turn = True
                    else:
                        if self.selected_piece is None:
                            if clicked_square == self.duck.position and not self.game.end:
                                self.select_piece(clicked_square)
                        elif self.selected_piece:
                            self.move_duck(clicked_square)

    def select_piece(self, square):
        if self.highlight_on:
            for move in self.legal_moves:
                if move.start == square:
                    self.highlights[move.end].color = (1, 0, 0, 1)
            if self.legal_duck_moves:
                for duck_move in self.legal_duck_moves:
                    if duck_move.start == square:
                        self.highlights[duck_move.end].color = (1, 0, 0, 1)

        self.selected_piece = self.pieces[square]
        self.selected_piece.size_hint = (.15, .15)
        self.square_from = square

    def deselect_piece(self):
        if self.highlight_on:
            for square in self.highlights.values():
                square.color = (1, 0, 0, 0)
        self.selected_piece.size_hint = (.125, .125)
        self.selected_piece = None
        self.square_from = None

    def execute_move(self, square_from, square_to):
        for move in self.legal_moves:
            if square_from == move.start and square_to == move.end:

                self.game.make_move(move)
                app = MDApp.get_running_app()
                turn = app.root.ids.game.ids.turn.text
                if turn == "Ruch Białego":
                    app.root.ids.game.ids.turn.text = "Ruch Białego (kaczka)"
                if turn == "Ruch Czarnego":
                    app.root.ids.game.ids.turn.text = "Ruch Czarnego (kaczka)"
                if move.piece_type == 'p' and (move.end[1] == "1" or move.end[1] == "8"):
                    app = MDApp.get_running_app()
                    app.root.ids.game.show_simple_dialog(move.piece_color)
                if move.captured_piece == "--":
                    normal_move_sound()
                else:
                    capture_move_sound()
                if self.notation_box is None:
                    self.notation_count += 1
                    self.notation_box = MDBoxLayout(adaptive_height=True)
                    self.notation_box_move_count = MDLabel(size_hint=(0.1, 1), color=[1, 1, 1, 1], halign="center", text=str(self.notation_count))
                    self.notation_box_move_white = MDLabel(size_hint=(0.45, 1), color=[1, 1, 1, 1], halign="center", text=square_from+square_to)
                    self.notation_box_move_black = MDLabel(size_hint=(0.45, 1), color=[1, 1, 1, 1], halign="center", text="")
                    self.notation_box.add_widget(self.notation_box_move_count)
                    self.notation_box.add_widget(self.notation_box_move_white)
                    self.notation_box.add_widget(self.notation_box_move_black)
                    self.parent.parent.parent.parent.ids.notation.add_widget(self.notation_box)
                    self.parent.parent.parent.parent.ids.scroll_notation.scroll_to(self.notation_box)
                else:
                    self.notation_box_move_black.text = square_from+square_to

                if square_from != square_to:
                    self.update_board()
                    self.next_player_turn = False
        else:
            self.deselect_piece()
            self.legal_duck_moves = self.game.generate_duck_moves()

    def place_duck(self, square_to):
        self.game.duck_place(square_to)
        duck_move_sound()
        self.update_board()
        self.legal_moves = self.game.generate_pseudo_legal_moves()
        if len(self.legal_moves) == 0:
            self.game.end = True
            self.game.whoToMove *= -1
            self.update_board()
        self.notation_box_move_white.text += " , " + square_to
        app = MDApp.get_running_app()
        turn = app.root.ids.game.ids.turn.text
        if turn == "Ruch Białego (kaczka)":
            app.root.ids.game.ids.turn.text = "Ruch Czarnego"
        if turn == "Ruch Czarnego (kaczka)":
            app.root.ids.game.ids.turn.text = "Ruch Białego"
        if self.is_black_engine == 1:
            Clock.schedule_once(self.bot_move_after_pause, .5)
        elif self.is_white_engine == 1:
            Clock.schedule_once(self.bot_move_before_pause, .5)

    def move_duck(self, square_to):
        for duck_move in self.legal_duck_moves:
            if duck_move.start == self.duck.position and duck_move.end == square_to:
                if self.game.whoToMove == 1:
                    self.notation_box_move_white.text += " , " + square_to
                if self.game.whoToMove == -1:
                    self.notation_box_move_black.text += " , " + square_to
                    self.notation_box = None
                    self.notation_box_move_count = None
                    self.notation_box_move_white = None
                    self.notation_box_move_black = None
                self.game.duck_move(duck_move)
                duck_move_sound()
                self.update_board()
                self.next_player_turn = True
        else:
            self.deselect_piece()
            self.legal_moves = self.game.generate_pseudo_legal_moves()
            app = MDApp.get_running_app()
            turn = app.root.ids.game.ids.turn.text
            if turn == "Ruch Białego (kaczka)":
                app.root.ids.game.ids.turn.text = "Ruch Czarnego"
            if turn == "Ruch Czarnego (kaczka)":
                app.root.ids.game.ids.turn.text = "Ruch Białego"
            if len(self.legal_moves) == 0:
                self.game.end = True
                self.game.whoToMove *= -1
                self.update_board()
        if self.is_black_engine == 1 and self.next_player_turn:
            Clock.schedule_once(self.bot_move_after_pause, .1)
        elif self.is_white_engine == 1 and self.next_player_turn:
            Clock.schedule_once(self.bot_move_before_pause, .1)

    def bot_move_after_pause(self, dt):
        if self.is_black_engine == 1 and self.legal_moves:
            temp_state = copy.deepcopy(self.game.state)
            temp_moves = copy.deepcopy(self.game.moves)
            temp_duck_moves = copy.deepcopy(self.game.duck_moves)
            temp_whoToMove = copy.deepcopy(self.game.whoToMove)
            temp_end = copy.deepcopy(self.game.end)
            temp_moves_point = copy.deepcopy(self.game.moves_point)
            temp_castle_rights_list = copy.deepcopy(self.game.castle_rights_list)
            temp_en_passant = copy.deepcopy(self.game.en_passant)
            temp_game = Game()
            temp_game.state = temp_state
            temp_game.moves = temp_moves
            temp_game.duck_moves = temp_duck_moves
            temp_game.whoToMove = temp_whoToMove
            temp_game.end = temp_end
            temp_game.moves_point = temp_moves_point
            temp_game.castle_rights_list = temp_castle_rights_list
            temp_game.en_passant = temp_en_passant

            move = search(temp_game, color="black")
            self.notation_box_move_black.text += move.start + move.end
            if move.captured_piece == "--":
                normal_move_sound()
            else:
                capture_move_sound()
            self.bot_move(move)

            Clock.schedule_once(self.bot_duck_move_after_pause, .1)

    def bot_duck_move_after_pause(self, dt):
        if not self.game.end:
            move = random_move_search(self.legal_duck_moves)
            self.notation_box_move_black.text += " , " + move.end
            self.notation_box = None
            self.notation_box_move_count = None
            self.notation_box_move_white = None
            self.notation_box_move_black = None
            self.duck_bot_move(move)
            app = MDApp.get_running_app()
            turn = app.root.ids.game.ids.turn.text
            if turn == "Ruch Białego":
                app.root.ids.game.ids.turn.text = "Ruch Czarnego"
            if turn == "Ruch Czarnego":
                app.root.ids.game.ids.turn.text = "Ruch Białego"
            duck_move_sound()

    def bot_move_before_pause(self, dt):
        if self.is_white_engine == 1 and self.legal_moves:
            temp_state = copy.deepcopy(self.game.state)
            temp_moves = copy.deepcopy(self.game.moves)
            temp_duck_moves = copy.deepcopy(self.game.duck_moves)
            temp_whoToMove = copy.deepcopy(self.game.whoToMove)
            temp_end = copy.deepcopy(self.game.end)
            temp_moves_point = copy.deepcopy(self.game.moves_point)
            temp_castle_rights_list = copy.deepcopy(self.game.castle_rights_list)
            temp_en_passant = copy.deepcopy(self.game.en_passant)
            temp_game = Game()
            temp_game.state = temp_state
            temp_game.moves = temp_moves
            temp_game.duck_moves = temp_duck_moves
            temp_game.whoToMove = temp_whoToMove
            temp_game.end = temp_end
            temp_game.moves_point = temp_moves_point
            temp_game.castle_rights_list = temp_castle_rights_list
            temp_game.en_passant = temp_en_passant

            move = search(temp_game, self.is_duck_on_board)
            if self.notation_box is None:
                self.notation_count += 1
                self.notation_box = MDBoxLayout(adaptive_height=True)
                self.notation_box_move_count = MDLabel(size_hint=(0.1, 1), color=[1, 1, 1, 1], halign="center",
                                                       text=str(self.notation_count))
                self.notation_box_move_white = MDLabel(size_hint=(0.45, 1), color=[1, 1, 1, 1], halign="center",
                                                       text=move.start + move.end)
                self.notation_box_move_black = MDLabel(size_hint=(0.45, 1), color=[1, 1, 1, 1], halign="center",
                                                       text="")
                self.notation_box.add_widget(self.notation_box_move_count)
                self.notation_box.add_widget(self.notation_box_move_white)
                self.notation_box.add_widget(self.notation_box_move_black)
                self.parent.parent.parent.parent.ids.notation.add_widget(self.notation_box)
                self.parent.parent.parent.parent.ids.scroll_notation.scroll_to(self.notation_box)
            else:
                self.notation_box_move_black.text = move.start + move.end
            if move.captured_piece == "--":
                normal_move_sound()
            else:
                capture_move_sound()
            self.bot_move(move)

            Clock.schedule_once(self.bot_duck_move_before_pause, .1)

    def bot_duck_move_before_pause(self, dt):
        if not self.game.end:
            move = random_move_search(self.legal_duck_moves)
            self.notation_box_move_white.text += " , " + move.end
            self.duck_bot_move(move)
            app = MDApp.get_running_app()
            turn = app.root.ids.game.ids.turn.text
            if turn == "Ruch Białego":
                app.root.ids.game.ids.turn.text = "Ruch Czarnego"
            if turn == "Ruch Czarnego":
                app.root.ids.game.ids.turn.text = "Ruch Białego"
            duck_move_sound()

