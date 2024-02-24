from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from data.database import show_data
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import IRightBodyTouch
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivymd.uix.button import MDFlatButton
from data import settings
from kivy.clock import Clock
import random
from data.database import wipe_data
import json



class ImageItemColor(ButtonBehavior, Image):
    pass


class ImageItemSource(ButtonBehavior, Image):
    pass


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass


class MainScreen(MDScreen):
    data_tables = None
    layout = None
    dialog = None

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.app = MDApp.get_running_app()
        self.menu_hue = None
        self.menu_color = None
        self.menu_dark_square = None
        self.menu_piece_style = None

    def show_alert_dialog(self):
        app = MDApp.get_running_app()
        if not self.dialog:
            self.dialog = MDDialog(
                title="Zresetować statystyki?",
                text="Wszystkie dane rozegranych parti zostaną usunięte.",
                buttons=[
                    MDFlatButton(
                        text="ANALUJ",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="USUŃ",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=self.reset_stats
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def reset_stats(self, *args):
        self.stats_reset()
        self.deselect()
        self.relogin()
        self.dialog.dismiss()

    def prep_piece_style(self):
        pieces = ["data/img/nW.png", "data/img/DD.png"]
        menu_items_piece_style = [
            {
                "viewclass": "ImageItemSource",
                "source": piece,
                "height": dp(50),
                "width": dp(20),
                "text": f"{piece}",
                "on_release": lambda x=piece: self.change_piece_style(x),
            } for piece in pieces]

        self.menu_piece_style = MDDropdownMenu(
            caller=self.drop_item_piece_style,
            items=menu_items_piece_style,
            position="auto",
            width_mult=4,
        )

    def prep_dark_square(self):
        colors = ["779455", "C3824C", "DA70D6"]
        menu_items_dark_square = [
            {
                "viewclass": "ImageItemColor",
                "color": color,
                "height": dp(50),
                "width": dp(20),
                "text": f"{color}",
                "on_release": lambda x=color: self.color_change_dark_square(x),
            } for color in colors]

        self.menu_dark_square = MDDropdownMenu(
            caller=self.drop_item_dark_square,
            items=menu_items_dark_square,
            position="auto",
            width_mult=4,
        )

    def prep_color(self):
        menu_items_color = [
            {
                "viewclass": "ImageItemColor",
                "color": color[1].get('A700'),
                "height": dp(50),
                "width": dp(20),
                "text": f"{color}",
                "on_release": lambda x=color: self.color_change(x),
            } for color in list(self.app.theme_cls.colors.items())[:-5]]

        self.menu_color = MDDropdownMenu(
            caller=self.drop_item_color,
            items=menu_items_color,
            position="auto",
            width_mult=4,
        )

    def prep_hue(self):
        menu_items_hue = [
            {
                "viewclass": "ImageItemColor",
                "color": self.app.theme_cls.colors[self.change_color.secondary_text][color],
                "height": dp(50),
                "width": dp(20),
                "text": f"{color}",
                "on_release": lambda x=(color, self.app.theme_cls.colors[self.change_color.secondary_text][color]): self.hue_change(x),
            } for color in self.app.theme_cls.colors[self.change_color.secondary_text]]

        self.menu_hue = MDDropdownMenu(
            caller=self.drop_item_hue,
            items=menu_items_hue,
            position="auto",
            width_mult=4,
        )

    def color_change_dark_square(self, color):
        self.drop_item_dark_square.md_bg_color = color
        self.menu_dark_square.dismiss()
        settings.dark_square_color = color
        with open('preferences.json', 'r') as plik:
            dane = json.load(plik)
        dane['dark_square'] = color

        with open('preferences.json', 'w') as plik:
            json.dump(dane, plik, indent=2)

    def change_piece_style(self, piece):
        self.drop_item_piece_style.icon = piece
        self.menu_piece_style.dismiss()

    def color_change(self, color):
        self.change_color.secondary_text = color[0]
        self.change_color.secondary_text_color = color[1].get('A700')
        self.drop_item_color.md_bg_color = color[1].get('A700')
        self.change_hue.secondary_text = 'A700'
        self.change_hue.secondary_text_color = color[1].get('A700')
        self.drop_item_hue.md_bg_color = color[1].get('A700')
        self.menu_color.dismiss()
        settings.color = color[1].get('A700')
        with open('preferences.json', 'r') as plik:
            dane = json.load(plik)
        dane['primary_color'] = color[0]

        with open('preferences.json', 'w') as plik:
            json.dump(dane, plik, indent=2)

        app = MDApp.get_running_app()
        app.theme_cls.primary_palette = color[0]

    def hue_change(self, color):
        self.change_hue.secondary_text = color[0]
        self.change_hue.secondary_text_color = color[1]
        self.drop_item_hue.md_bg_color = color[1]
        self.menu_hue.dismiss()
        settings.hue = color[0]
        with open('preferences.json', 'r') as plik:
            dane = json.load(plik)
        dane['hue'] = color[0]

        with open('preferences.json', 'w') as plik:
            json.dump(dane, plik, indent=2)

        app = MDApp.get_running_app()
        app.theme_cls.primary_hue = color[0]

    def apply_changes(self):
        self.app.theme_cls.primary_palette = self.change_color.secondary_text
        self.app.theme_cls.primary_hue = self.change_hue.secondary_text
        self.settings_nav.switch_tab("Theming")
    
    def deselect(self):
        self.nav_bar.deselect_item(self.logout)

    @staticmethod
    def toggle_highlights():
        settings.highlights = not settings.highlights

        with open('preferences.json', 'r') as plik:
            dane = json.load(plik)
        dane['highlight'] = str(settings.highlights)

        with open('preferences.json', 'w') as plik:
            json.dump(dane, plik, indent=2)

    @staticmethod
    def toggle_sounds():
        settings.sounds = not settings.sounds

        with open('preferences.json', 'r') as plik:
            dane = json.load(plik)
        dane['sound'] = str(settings.sounds)

        with open('preferences.json', 'w') as plik:
            json.dump(dane, plik, indent=2)

    def initialize_board(self):
        self.parent.ids.game.ids.board.initialize_board()

    def initialize_bot_random(self):
        bot = random.choice([self.initialize_bot_black, self.initialize_bot_white])
        bot()

    def initialize_bot_black(self):
        self.parent.ids.game.ids.board.is_black_engine = 1
        self.parent.ids.game.ids.board.is_white_engine = -1
        self.parent.ids.game.ids.board.player_side = "Bialy"
        self.parent.ids.game.ids.turn.text = "Ruch Białego"
        self.parent.ids.game.ids.play_as.text = "Grasz jako Biały"

    def initialize_bot_white(self):
        self.parent.ids.game.ids.board.is_white_engine = 1
        self.parent.ids.game.ids.board.is_black_engine = -1
        self.parent.ids.game.ids.board.player_side = "Czarny"
        self.parent.ids.game.ids.turn.text = "Ruch Białego"
        self.parent.ids.game.ids.play_as.text = "Grasz jako Czarny"
        Clock.schedule_once(self.parent.ids.game.ids.board.bot_move_before_pause, 1.5)

    def initialize_player(self):
        self.parent.ids.game.ids.board.is_black_engine = -1
        self.parent.ids.game.ids.board.is_white_engine = -1
        self.parent.ids.game.ids.turn.text = "Ruch Białego"
        self.parent.ids.game.ids.play_as.text = ""

    def initialize_stats(self):
        self.layout = AnchorLayout()
        self.data_tables = MDDataTable(
            size_hint=(.9, .9),
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("No.", dp(30), None, "Custom tooltip"),
                ("Gracz", dp(30)),
                ("Przeciwnik", dp(30)),
                ("Kolor", dp(30)),
                ("Wynik", dp(30)),
                ("Ilość ruchów", dp(30)),
                ("Data", dp(60)),
            ],
        )
        self.layout.add_widget(self.data_tables)
        self.games_list.add_widget(self.layout)

    def update_stats(self):
        if settings.logged == "gracz":
            query = show_data("SELECT chessgames.id, players.name AS player_name, chessgames.opponent, chessgames.player_side, chessgames.result, chessgames.moves_count, SUBSTR(chessgames.date, 1, LENGTH(chessgames.date) - 7) AS trimmed_date FROM chessgames JOIN players ON chessgames.player = players.id WHERE chessgames.player=?", (
            settings.logged_id,))
            if len(query) != len(self.data_tables.row_data):
                self.data_tables.row_data = query

            games_count_query = show_data("SELECT * FROM chessgames WHERE player=?", (settings.logged_id,))
            games_count = len(games_count_query) if games_count_query else "--"
            if games_count_query:
                games_moves_max = show_data("SELECT moves_count FROM chessgames WHERE player=? ORDER BY moves_count", (settings.logged_id,))[-1][0]
                games_moves_min = show_data("SELECT moves_count FROM chessgames WHERE player=? ORDER BY moves_count", (settings.logged_id,))[0][0]
                games_win_white = show_data("SELECT * FROM chessgames WHERE (player_side='Bialy' AND result='1-0')").__len__()
                games_win_black = show_data("SELECT * FROM chessgames WHERE (player_side='Czarny' AND result='0-1')").__len__()
                self.ids.games_moves_max.text = str(games_moves_max) if games_count else "--"
                self.ids.games_moves_min.text = str(games_moves_min) if games_count else "--"
                self.ids.games_win_white.text = str(games_win_white) if games_count else "--"
                self.ids.games_win_black.text = str(games_win_black) if games_count else "--"
                self.ids.games_win.text = str(games_win_white + games_win_black) if games_count else "--"
            self.ids.games_count.text = str(games_count)

    def stats_reset(self):
        wipe_data()

    def relogin(self):
        Clock.schedule_once(self.relogin_callback, .5)

    def relogin_callback(self, dt):
        app = MDApp.get_running_app()
        app.root.ids.login.login()
        app.root.ids.login.wipe_querys()

    def load_pref(self):
        f = open('preferences.json')
        data = json.load(f)
        if data["highlight"] == "True":
            self.ids.highlight.active = True
        elif data["highlight"] == "False":
            self.ids.highlight.active = False

        self.ids.drop_item_dark_square.md_bg_color = data["dark_square"]
        settings.dark_square_color = data["dark_square"]

        app = MDApp.get_running_app()
        app.theme_cls.primary_palette = data["primary_color"]
        app.theme_cls.primary_hue = data["hue"]

        app.root.ids.menu.change_color.secondary_text = data["primary_color"]
        app.root.ids.menu.change_hue.secondary_text = data["hue"]

        if data["sound"] == "True":
            self.ids.sounds.active = True
        elif data["sound"] == "False":
            self.ids.sounds.active = False


Builder.load_file("data/screens/menu_screen.kv")
