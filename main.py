import os
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pathlib import Path
import toga
from toga.style import Pack
import json

class FitTrackMateApp(toga.App):
    def __init__(self, formal_name, package_name):
        super().__init__(formal_name, package_name)

        # A név tárolása
        self._name = None

    def startup(self):
        # Fájl ellenőrzése és név beolvasása, ha van ilyen
        if os.path.exists("name.json"):
            with open("name.json", "r") as f:
                self._name = json.loads(f.read())["name"]

        # A fő ablak létrehozása
        self.main_window = toga.MainWindow(title=self.formal_name)

        if self._name:
            # Ha van elmentett név, akkor megjelenítjük az üdvözlő üzenetet
            self.show_welcome_screen()
        else:
            # Ha nincs elmentett név, akkor kérünk egyet
            self.ask_for_name()

    def ask_for_name(self):
        # Szöveges beviteli mező
        self.name_input = toga.TextInput()

        # Gomb az adat beküldésére és az üzenet kezelésére
        self.submit_button = toga.Button('Submit', on_press=self.submit_name)

        # Készítsünk el egy elrendezést (box layout)
        self.box = toga.Box(children=[toga.Label('Please enter your name'), self.name_input, self.submit_button],
                            style=Pack(direction='column', padding=20))

        # A box layout-ot rendeljük az ablak közepére
        self.main_window.content = self.box

        # A fő ablak megjelenítése
        self.main_window.show()

    def submit_name(self, widget):
        # A gomb lenyomásakor kezeljük az üdvözlő üzenet megjelenítését
        name = self.name_input.value
        if name:
            # A név tárolása
            self._name = name

            # A fájlba írás
            with open("name.json", "w") as f:
                f.write(json.dumps({"name": name}))

            # Az üdvözlő üzenet megjelenítése az ablakban
            self.show_welcome_screen()

    def show_welcome_screen(self):
        # Üdvözlő üzenet
        self.greeting_label = toga.Label(f"Welcome, {self._name}!")

        # Készítsünk el egy elrendezést (box layout)
        self.box = toga.Box(children=[self.greeting_label],
                            style=Pack(direction='column', padding=20))

        # A box layout-ot rendeljük az ablak közepére
        self.main_window.content = self.box


def main():
    return FitTrackMateApp('FitTrackMate', 'org.fittrackmate')

if __name__ == '__main__':
    app = main()
    app.main_loop()