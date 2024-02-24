from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from data import settings
from kivymd.uix.list import OneLineAvatarListItem
from kivy.properties import StringProperty
from kivymd.uix.button import MDFlatButton

from data.engine.constants import NOTATION_TO_GAME_STATE

Builder.load_file("data/screens/game_screen.kv")


class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()


class GameScreen(MDScreen):
    simple_dialog = None
    alert_dialog = None

    def show_simple_dialog(self, color):
        if self.simple_dialog:
            self.simple_dialog = None
        if not self.simple_dialog:
            self.simple_dialog = MDDialog(
                title="Wybór promocji pionka",
                type="simple",
                items=[
                    Item(source="data/img/q"+color+".png", on_release=self.item_selected),
                    Item(source="data/img/r"+color+".png", on_release=self.item_selected),
                    Item(source="data/img/n"+color+".png", on_release=self.item_selected),
                    Item(source="data/img/b"+color+".png", on_release=self.item_selected),
                ],
            )
        self.simple_dialog.open()

    def show_alert_dialog(self):
        app = MDApp.get_running_app()
        if not self.alert_dialog:
            self.alert_dialog = MDDialog(
                title="Przejść do menu?",
                text="Przejście do menu nie zapisze niedokończonej partie",
                buttons=[
                    MDFlatButton(
                        text="ANALUJ",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="MENU",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=self.go_to_menu
                    ),
                ],
            )
        self.alert_dialog.open()

    def close_dialog(self, *args):
        self.alert_dialog.dismiss()

    def go_to_menu(self, *args):
        self.board.unbind_keys()
        self.parent.ids.menu.update_stats()
        self.clear_notation()
        self.parent.current = 'main'
        self.alert_dialog.dismiss()

    def item_selected(self, instance):
        app = MDApp.get_running_app()
        move = app.root.ids.game.ids.board.game.moves[-1]
        move.piece_type = instance.source[9:10]
        move.promotion_piece = instance.source[9:11]
        end = NOTATION_TO_GAME_STATE[move.end]
        app.root.ids.game.ids.board.game.state[end[0]][end[1]] = move.piece_type + move.piece_color
        app.root.ids.game.ids.board.update_board()
        settings.promotion = instance.source[9:10]

    def clear_notation(self):
        all_widgets = [widget for widget in self.ids.notation.children]
        for widget in all_widgets:
            self.ids.notation.remove_widget(widget)

    def toggle_highlights(self):
        settings.highlights = not settings.highlights
        self.ids.board.highlight_on = not self.ids.board.highlight_on

    def deselect_piece(self):
        if self.ids.board.selected_piece is not None:
            self.ids.board.deselect_piece()

    def flip_board(self):
        self.ids.board.game.flip_board()
        self.ids.board.update_board()
        self.ids.board.legal_moves = self.ids.board.game.generate_pseudo_legal_moves()
        self.ids.board.legal_duck_moves = self.ids.board.game.generate_duck_moves()

