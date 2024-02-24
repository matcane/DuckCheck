from data import settings
from data.engine.constants import GAME_STATE_TO_NOTATION, NOTATION_TO_GAME_STATE, FILES, RANKS, GAME_STATE_TO_NOTATION_FLIPPED, NOTATION_TO_GAME_STATE_FLIPPED


class Move:
    def __init__(self, piece, captured_piece, start, end, promotion=False, promotion_piece="q", castle=False, castle_side=None, flipped=False, en_passant=False):
        self.piece = piece
        self.piece_type = piece[0]
        self.piece_color = piece[1]
        self.start = GAME_STATE_TO_NOTATION[start] if not flipped else GAME_STATE_TO_NOTATION_FLIPPED[start]
        self.end = GAME_STATE_TO_NOTATION[end] if not flipped else GAME_STATE_TO_NOTATION_FLIPPED[end]
        self.captured_piece = captured_piece
        self.captured_piece_type = captured_piece[0]
        self.captured_piece_color = captured_piece[1]
        self.promotion = promotion
        self.promotion_piece = promotion_piece + self.piece_color
        self.castle = castle
        self.castle_side = castle_side
        self.en_passant = en_passant


class Duck:
    def __init__(self, duck, captured_piece, start, end, flipped=False):
        self.duck = duck
        self.captured_piece = captured_piece
        self.start = GAME_STATE_TO_NOTATION.get(start, None) if not flipped else GAME_STATE_TO_NOTATION_FLIPPED.get(start, None)
        self.end = GAME_STATE_TO_NOTATION[end] if not flipped else GAME_STATE_TO_NOTATION_FLIPPED[end]


class CastleRights:
    def __init__(self, white_king_side=True, black_king_side=True, white_queen_side=True, black_queen_side=True):
        self.white_king_side = white_king_side
        self.black_king_side = black_king_side
        self.white_queen_side = white_queen_side
        self.black_queen_side = black_queen_side


class Game:
    def __init__(self):
        self.state = [
            ['rB', 'nB', 'bB', 'qB', 'kB', 'bB', 'nB', 'rB'],
            ['pB', 'pB', 'pB', 'pB', 'pB', 'pB', 'pB', 'pB'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['pW', 'pW', 'pW', 'pW', 'pW', 'pW', 'pW', 'pW'],
            ['rW', 'nW', 'bW', 'qW', 'kW', 'bW', 'nW', 'rW']
        ]
        self.moves = []
        self.duck_moves = []
        self.whoToMove = 1
        self.end = False
        self.moves_point = None
        self.castle_rights_list = [CastleRights(True, True, True, True)]
        self.flipped = False
        self.en_passant = None

    def show(self):
        for row in self.state:
            print(row)

    def flip_board(self):
        self.state.reverse()
        for row in self.state:
            row.reverse()
        self.flipped = not self.flipped

    def get_pos(self, notation):
        if self.flipped:
            return NOTATION_TO_GAME_STATE_FLIPPED[notation]
        else:
            return NOTATION_TO_GAME_STATE[notation]

    def flipped_check(self, start, end):
        if self.flipped:
            start = FILES[start[0]] + RANKS[start[1]]
            end = FILES[end[0]] + RANKS[end[1]]
        return start, end

    def make_move(self, move):
        if self.square_may_be_attacked(move):
            self.push(move)
            if move.piece_type == 'p' and (move.end[1] == "1" or move.end[1] == "8"):
                self.pawn_promotion(move)
            if move.en_passant:
                self.en_passant_move(move)
            self.en_passant_rights(move)
            self.castle_rights(move)
            self.castle(move)


    def pawn_promotion(self, move):
        move.promotion = True
        end = self.get_pos(move.end)
        if move.promotion:
            self.state[end[0]][end[1]] = settings.promotion + move.piece_color

    def en_passant_rights(self, move):
        start = self.get_pos(move.start)
        end = self.get_pos(move.end)
        if move.piece_type == 'p' and abs(end[0] - start[0]) == 2:
            if move.piece_color == "W":
                self.en_passant = end[0] + 1, end[1]
            if move.piece_color == "B":
                self.en_passant = end[0] - 1, end[1]
        else:
            self.en_passant = None

    def en_passant_move(self, move):
        start = self.get_pos(move.start)
        end = self.get_pos(move.end)
        if move.piece_type == 'p' and move.piece_color == "W" and (end[0], end[1]) == self.en_passant:
            self.state[end[0] + 1][end[1]] = "--"
        if move.piece_type == 'p' and move.piece_color == "B" and (end[0], end[1]) == self.en_passant:
            self.state[end[0] - 1][end[1]] = "--"

    def castle(self, move):
        start = self.get_pos(move.start)
        end = self.get_pos(move.end)

        if move.castle:
            rook_start_col = end[1] - 1 if end[1] - start[1] == 2 else end[1] + 1
            rook_end_col = end[1] + 1 if end[1] - start[1] == 2 else end[1] - 2

            self.state[end[0]][rook_start_col] = self.state[end[0]][rook_end_col]
            self.state[end[0]][rook_end_col] = '--'

    def castle_rights(self, move):
        white_king_side = self.castle_rights_list[-1].white_king_side
        black_king_side = self.castle_rights_list[-1].black_king_side
        white_queen_side = self.castle_rights_list[-1].white_queen_side
        black_queen_side = self.castle_rights_list[-1].black_queen_side
        castle_rights = CastleRights(white_king_side, black_king_side, white_queen_side, black_queen_side)
        if move.piece == 'kW':
            castle_rights.white_king_side = False
            castle_rights.white_queen_side = False
        elif move.piece == 'kB':
            castle_rights.black_king_side = False
            castle_rights.black_queen_side = False
        elif move.piece == 'rW':
            if move.start == "a1":
                castle_rights.white_queen_side = False
            elif move.start == "h1":
                castle_rights.white_king_side = False
        elif move.piece == 'rB':
            if move.start == "a8":
                castle_rights.black_queen_side = False
            elif move.start == "h8":
                castle_rights.black_king_side = False
        elif move.captured_piece == "rW":
            if move.end == "a1":
                castle_rights.white_queen_side = False
            elif move.end == "h1":
                castle_rights.white_king_side = False
        elif move.captured_piece == 'rB':
            if move.end == "a8":
                castle_rights.black_queen_side = False
            elif move.end == "h8":
                castle_rights.black_king_side = False

        self.castle_rights_list.append(castle_rights)

    def duck_place(self, end):
        pos = self.get_pos(end)
        if self.state[pos[0]][pos[1]] == '--':
            self.state[pos[0]][pos[1]] = 'DD'
            self.whoToMove *= -1
            self.duck_moves.append(Duck('DD', '--', pos, pos, flipped=self.flipped))

    def duck_move(self, duck_move):
        if self.square_is_empty(duck_move.end):
            self.duck_push(duck_move)

    def unmake_move(self):
        equal_moves = True if len(self.moves) == len(self.duck_moves) else False
        if self.moves:
            if self.duck_moves and equal_moves:
                duck_move = self.duck_moves.pop()
                self.duck_pop(duck_move)
                move = self.moves.pop()
                self.pop(move)
            else:
                move = self.moves.pop()
                self.pop(move)
        if len(self.castle_rights_list) > 1:
            self.castle_rights_list.pop()

        self.moves_point = None

    def prev_last(self):
        while self.moves:
            self.prev_move()
            if self.moves_point == 0:
                break

    def next_last(self):
        while self.moves_point is not None:
            self.next_move()

    def prev_move(self):
        equal_moves = True if len(self.moves) == len(self.duck_moves) else False
        if self.moves:
            if self.moves_point is not None and self.moves_point > 0:
                self.moves_point -= 1
                if self.duck_moves:
                    self.duck_prev(self.duck_moves[self.moves_point])
                    self.pop(self.moves[self.moves_point])
                else:
                    self.pop(self.moves[self.moves_point])
            if self.moves_point is None:
                self.moves_point = len(self.moves)
                self.moves_point -= 1
                if self.duck_moves and equal_moves:
                    self.duck_prev(self.duck_moves[self.moves_point])
                    self.pop(self.moves[self.moves_point])
                else:
                    self.pop(self.moves[self.moves_point])

    def next_move(self):
        if self.moves_point is not None and self.moves_point <= len(self.moves) - 1:
            self.next(self.moves[self.moves_point])
            if self.duck_moves and self.moves_point <= len(self.duck_moves) - 1:
                self.duck_next(self.duck_moves[self.moves_point])
            self.moves_point += 1
        if self.moves_point == len(self.moves):
            self.moves_point = None

    def get_duck_position(self):
        for row_index, row in enumerate(self.state):
            for col_index, col in enumerate(row):
                if self.state[row_index][col_index] == 'DD':
                    return row_index, col_index

    def get_white_king_position(self):
        for row_index, row in enumerate(self.state):
            for col_index, col in enumerate(row):
                if self.state[row_index][col_index] == 'kW':
                    return row_index, col_index

    def get_black_king_position(self):
        for row_index, row in enumerate(self.state):
            for col_index, col in enumerate(row):
                if self.state[row_index][col_index] == 'kB':
                    return row_index, col_index

    def square_is_empty(self, end):
        notation = self.get_pos(end)
        if self.state[notation[0]][notation[1]] == '--':
            return True
        else:
            return False

    def square_under_attack(self, square):
        self.whoToMove *= -1
        moves = self.generate_pseudo_legal_moves()
        self.whoToMove *= -1
        for move in moves:
            if move.end == square:
                return True
        return False

    def square_may_be_attacked(self, move):
        if self.square_is_empty(move.end) or self.move_can_be_made(move.captured_piece_color):
            return True
        else:
            return False

    def move_can_be_made(self, piece_color):
        if (self.whoToMove == 1 and piece_color == "B") or (self.whoToMove == -1 and piece_color == "W"):
            return True
        else:
            return False

    def push(self, move):
        if move.captured_piece in ["kW", "kB"]:
            self.end = True
        end = self.get_pos(move.end)
        start = self.get_pos(move.start)
        self.state[end[0]][end[1]] = move.piece
        self.state[start[0]][start[1]] = "--"
        self.moves.append(move)

    def duck_push(self, move):
        start = self.get_pos(move.start)
        end = self.get_pos(move.end)
        self.state[end[0]][end[1]] = move.duck
        self.state[start[0]][start[1]] = move.captured_piece
        self.duck_moves.append(move)
        self.whoToMove *= -1

    def pop(self, move):
        start = self.get_pos(move.start)
        end = self.get_pos(move.end)

        self.state[end[0]][end[1]] = move.captured_piece
        self.state[start[0]][start[1]] = move.piece
        if move.promotion:
            self.state[start[0]][start[1]] = 'p' + move.piece_color
        if move.castle:
            if end[1] - start[1] == 2:
                self.state[end[0]][end[1] + 1] = self.state[end[0]][end[1] - 1]
                self.state[end[0]][end[1] - 1] = '--'
            else:
                self.state[end[0]][end[1] - 2] = self.state[end[0]][end[1] + 1]
                self.state[end[0]][end[1] + 1] = '--'

        if move.en_passant:
            self.state[end[0]][end[1]] = "--"
            if move.piece_color == "W":
                self.state[end[0] + 1][end[1]] = move.captured_piece
            if move.piece_color == "B":
                self.state[end[0] - 1][end[1]] = move.captured_piece

    def duck_pop(self, move):
        start = self.get_pos(move.start)
        end = self.get_pos(move.end)
        if self.duck_moves and self.moves_point != 0:
            self.state[end[0]][end[1]] = move.captured_piece
            self.state[start[0]][start[1]] = move.duck
            self.whoToMove *= -1
        if len(self.duck_moves) == 0 or self.moves_point == 0:
            self.state[start[0]][start[1]] = move.captured_piece
            self.whoToMove *= -1

    def next(self, move):
        start = self.get_pos(move.start)
        end = self.get_pos(move.end)
        self.state[end[0]][end[1]] = move.piece
        self.state[start[0]][start[1]] = "--"
        if move.promotion:
            self.state[end[0]][end[1]] = move.promotion_piece
        if move.castle:
            self.castle(move)

    def duck_prev(self, move):
        start = self.get_pos(move.start)
        end = self.get_pos(move.end)
        if self.duck_moves and self.moves_point != 0:
            self.state[end[0]][end[1]] = move.captured_piece
            self.state[start[0]][start[1]] = move.duck
        if len(self.duck_moves) == 0 or self.moves_point == 0:
            self.state[start[0]][start[1]] = move.captured_piece

    def duck_next(self, move):
        start = self.get_pos(move.start)
        end = self.get_pos(move.end)
        self.state[end[0]][end[1]] = move.duck
        self.state[start[0]][start[1]] = move.captured_piece
        if start == end:
            self.state[start[0]][start[1]] = move.duck

    def generate_pseudo_legal_moves(self):
        generated_moves = []
        if not self.end:
            for row_index, row in enumerate(self.state):
                for col_index, col in enumerate(row):
                    self.get_moves(row_index, col_index, generated_moves)
        return generated_moves

    def generate_duck_moves(self):
        if self.end:
            return []

        return [Duck('DD', '--', self.get_duck_position(), (row_index, col_index), flipped=self.flipped)
                for row_index, row in enumerate(self.state)
                for col_index, col in enumerate(row)
                if self.state[row_index][col_index] == '--']

    def get_moves(self, row, col, generated_moves):
        piece = self.state[row][col]
        piece_type = piece[0]
        piece_color = piece[1]
        if not self.move_can_be_made(piece_color):
            if piece_type == 'p' and piece_color == "W":
                self.get_white_pawn_moves(row, col, generated_moves)
            if piece_type == 'p' and piece_color == "B":
                self.get_black_pawn_moves(row, col, generated_moves)
            if piece_type == 'r':
                self.get_rook_moves(row, col, generated_moves)
            if piece_type == 'n':
                self.get_knight_moves(row, col, generated_moves)
            if piece_type == 'b':
                self.get_bishop_moves(row, col, generated_moves)
            if piece_type == 'q':
                self.get_queen_moves(row, col, generated_moves)
            if piece_type == 'k':
                self.get_king_moves(row, col, generated_moves)

    def get_move_line(self, row, col, moves, direction_row, direction_col, depth=7):
        piece_position = (row, col)
        for i in range(1, depth + 1):
            new_row, new_col = row + i * direction_row, col + i * direction_col
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.state[new_row][new_col] == "--":
                    move_to = (new_row, new_col)
                    move = Move(self.state[row][col], self.state[new_row][new_col], piece_position, move_to, flipped=self.flipped)
                    moves.append(move)
                elif self.move_can_be_made(self.state[new_row][new_col][1]):
                    move_to = (new_row, new_col)
                    move = Move(self.state[row][col], self.state[new_row][new_col], piece_position, move_to, flipped=self.flipped)
                    moves.append(move)
                    break
                else:
                    break

    def get_pawn_moves(self, row, col, moves, direction, enemy_color, initial_row):
        piece_position = (row, col)
        new_row = row + direction
        if self.state[new_row][col] == "--":
            move_to = (new_row, col)
            move = Move(self.state[row][col], self.state[new_row][col], piece_position, move_to, flipped=self.flipped)
            moves.append(move)
            if row == initial_row and self.state[new_row + direction][col] == "--":
                move_to = (new_row + direction, col)
                move = Move(self.state[row][col], self.state[new_row + direction][col], piece_position, move_to, flipped=self.flipped)
                moves.append(move)

        if 0 <= new_row < 8:
            if 0 <= col - 1 < 8 and (self.state[new_row][col - 1][1] == enemy_color):
                move_to = (new_row, col - 1)
                move = Move(self.state[row][col], self.state[new_row][col - 1], piece_position, move_to, flipped=self.flipped)
                moves.append(move)
            elif (new_row, col - 1) == self.en_passant and self.state[new_row][col-1] != "DD":
                move_to = (new_row, col - 1)
                if enemy_color == "B":
                    move = Move(self.state[row][col], self.state[new_row + 1][col - 1], piece_position, move_to, flipped=self.flipped, en_passant=True)
                if enemy_color == "W":
                    move = Move(self.state[row][col], self.state[new_row - 1][col - 1], piece_position, move_to, flipped=self.flipped, en_passant=True)
                moves.append(move)
            if 0 <= col + 1 < 8 and (self.state[new_row][col + 1][1] == enemy_color):
                move_to = (new_row, col + 1)
                move = Move(self.state[row][col], self.state[new_row][col + 1], piece_position, move_to, flipped=self.flipped)
                moves.append(move)
            elif (new_row, col + 1) == self.en_passant and self.state[new_row][col+1] != "DD":
                move_to = (new_row, col + 1)
                if enemy_color == "B":
                    move = Move(self.state[row][col], self.state[new_row + 1][col + 1], piece_position, move_to, flipped=self.flipped, en_passant=True)
                if enemy_color == "W":
                    move = Move(self.state[row][col], self.state[new_row - 1][col + 1], piece_position, move_to, flipped=self.flipped, en_passant=True)
                moves.append(move)

    def get_white_pawn_moves(self, row, col, moves):
        self.get_pawn_moves(row, col, moves, -1, 'B', 6)

    def get_black_pawn_moves(self, row, col, moves):
        self.get_pawn_moves(row, col, moves, 1, 'W', 1)

    def get_rook_moves(self, row, col, moves):
        self.get_move_line(row, col, moves, 0, -1)
        self.get_move_line(row, col, moves, 0, 1)
        self.get_move_line(row, col, moves, -1, 0)
        self.get_move_line(row, col, moves, 1, 0)

    def get_knight_moves(self, row, col, moves):
        self.get_move_line(row, col, moves, -2, -1, 1)
        self.get_move_line(row, col, moves, -1, -2, 1)
        self.get_move_line(row, col, moves, 1, -2, 1)
        self.get_move_line(row, col, moves, 2, -1, 1)
        self.get_move_line(row, col, moves, 2, 1, 1)
        self.get_move_line(row, col, moves, 1, 2, 1)
        self.get_move_line(row, col, moves, -1, 2, 1)
        self.get_move_line(row, col, moves, -2, 1, 1)

    def get_bishop_moves(self, row, col, moves):
        self.get_move_line(row, col, moves, -1, -1)
        self.get_move_line(row, col, moves, 1, -1)
        self.get_move_line(row, col, moves, -1, 1)
        self.get_move_line(row, col, moves, 1, 1)

    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        self.get_move_line(row, col, moves, -1, -1, 1)
        self.get_move_line(row, col, moves, 0, -1, 1)
        self.get_move_line(row, col, moves, 1, -1, 1)
        self.get_move_line(row, col, moves, 1, 0, 1)
        self.get_move_line(row, col, moves, 1, 1, 1)
        self.get_move_line(row, col, moves, 0, 1, 1)
        self.get_move_line(row, col, moves, -1, 1, 1)
        self.get_move_line(row, col, moves, -1, 0, 1)
        self.get_castle_moves(row, col, moves)

    def get_castle_moves(self, row, col, moves):
        if (self.whoToMove == 1 and self.castle_rights_list[-1].white_king_side) or (self.whoToMove == -1 and self.castle_rights_list[-1].black_king_side):
            king_side_one = (row, col + 1) if not self.flipped else (row, col - 1)
            king_side_two = (row, col + 2) if not self.flipped else (row, col - 2)
            change = self.state[row][col + 2] if not self.flipped else self.state[row][col - 2]
            if self.square_is_empty(GAME_STATE_TO_NOTATION[king_side_one]) and self.square_is_empty(GAME_STATE_TO_NOTATION[king_side_two]):
                moves.append(Move(self.state[row][col], change, (row, col), king_side_two, castle=True))

        if (self.whoToMove == 1 and self.castle_rights_list[-1].white_queen_side) or (self.whoToMove == -1 and self.castle_rights_list[-1].black_queen_side):
            king_side_one = (row, col - 1) if not self.flipped else (row, col + 1)
            king_side_two = (row, col - 2) if not self.flipped else (row, col + 2)
            king_side_three = (row, col - 3) if not self.flipped else (row, col + 3)
            change = self.state[row][col - 2] if not self.flipped else self.state[row][col + 2]
            if self.square_is_empty(GAME_STATE_TO_NOTATION[king_side_one]) and self.square_is_empty(GAME_STATE_TO_NOTATION[king_side_two]) and self.square_is_empty(GAME_STATE_TO_NOTATION[king_side_three]):
                moves.append(Move(self.state[row][col], change, (row, col), king_side_two, castle=True))
