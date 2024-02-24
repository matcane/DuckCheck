from kivymd.app import MDApp
from data.database import initialize_db
from kivy.core.window import Window
import os, sys
from kivy.resources import resource_add_path, resource_find


class DuckApp(MDApp):
    window = Window
    window.minimum_width = 800
    window.minimum_height = 600

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        initialize_db()


if __name__ == '__main__':
    try:
        if hasattr(sys, '_MEIPASS'):
            resource_add_path(os.path.join(sys._MEIPASS))
        app = DuckApp()
        app.run()
    except Exception as e:
        print(e)
        input("Press enter.")
