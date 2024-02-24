from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.app import MDApp
from data.database import show_data, insert_data
from data import settings
import json


class LoginScreen(MDScreen):
    def wipe_querys(self):
        app = MDApp.get_running_app()
        app.root.ids.menu.games_moves_max.text = "--"
        app.root.ids.menu.games_moves_min.text = "--"
        app.root.ids.menu.games_count.text = "--"
        app.root.ids.menu.games_win_white.text = "--"
        app.root.ids.menu.games_win_black.text = "--"
        app.root.ids.menu.games_win.text = "--"

    def login(self):
        name = "Gracz".lower()
        app = MDApp.get_running_app()
        app.root.current = 'main'
        exists = show_data("SELECT * FROM players WHERE name=?", (name,))
        if not exists:
            insert_data("INSERT INTO players VALUES (NULL, ?)", (name,))
        player_id = show_data("SELECT * FROM players WHERE name=?", (name,))[0][0]
        settings.logged = name
        settings.logged_id = player_id
        try:
            with open('preferences.json', 'r') as plik:
                dane = json.load(plik)
        except FileNotFoundError:
            dane = {
                "highlight": "True",
                "sound": "True",
                "dark_square": "779455",
                "primary_color": "Blue",
                "hue": "700"
            }
            with open('preferences.json', 'w') as plik:
                json.dump(dane, plik, indent=2)
        app.root.ids.menu.load_pref()
        if name == "gracz":
            games_count_query = show_data("SELECT * FROM chessgames WHERE player=?", (player_id,))
            games_count = len(games_count_query) if games_count_query else "--"
            if games_count_query:
                games_moves_max = show_data("SELECT moves_count FROM chessgames WHERE player=? ORDER BY moves_count", (player_id,))[-1][0]
                games_moves_min = show_data("SELECT moves_count FROM chessgames WHERE player=? ORDER BY moves_count", (player_id,))[0][0]
                games_win_white = show_data("SELECT * FROM chessgames WHERE (player_side='Bialy' AND result='1-0')").__len__()
                games_win_black = show_data("SELECT * FROM chessgames WHERE (player_side='Czarny' AND result='0-1')").__len__()
                app.root.ids.menu.games_moves_max.text = str(games_moves_max) if games_count else "--"
                app.root.ids.menu.games_moves_min.text = str(games_moves_min) if games_count else "--"
                app.root.ids.menu.games_win_white.text = str(games_win_white) if games_count else "--"
                app.root.ids.menu.games_win_black.text = str(games_win_black) if games_count else "--"
                app.root.ids.menu.games_win.text = str(games_win_white + games_win_black) if games_count else "--"
            app.root.ids.menu.games_count.text = str(games_count)
        else:
            app.root.ids.menu.games_moves_max.text = "--"
            app.root.ids.menu.games_moves_min.text = "--"
            app.root.ids.menu.games_count.text = "--"

        app.root.ids.menu.dashboard.text = ""
        app.root.ids.menu.nav_bar.set_current_selected_item(0)
        app.root.ids.menu.initialize_stats()
        app.root.ids.menu.update_stats()



Builder.load_file("data/screens/login_screen.kv")
