import os
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pathlib import Path
import toga
from toga.style import Pack
import json
import datetime

def save_training_data(data):
    try:
        with open('training_data.json', 'w') as file:
            file.write(json.dumps(data))

    except Exception as e:
        print(f'Error saving data: {e}')


def load_trainingData():
    try:
        with open('training-data', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data
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

    def show_welcome_screen(self, widget=None):
        # Üdvözlő üzenet
        self.greeting_label = toga.Label(f"Welcome, {self._name}!")

        #főmenü gombo
        button1 = toga.Button('Training register', on_press=self.handle_training_entry)
        button2 = toga.Button('Weight register', on_press=self.handle_weight_entry)
        button3 = toga.Button('Training track', on_press=self.handle_training_statistics)
        button4 = toga.Button('Weight track', on_press=self.handle_weight_statistics)
        button5 = toga.Button('Options', on_press=self.handle_settings)
        #Elrendezés
        self.box = toga.Box(children=[self.greeting_label, button1, button2, button3, button4, button5],
                            style=Pack(direction='column', padding=20))

        # A box layout-ot rendeljük az ablak közepére
        self.main_window.content = self.box
    pass
    # Gomb kezelő függvények
    def handle_training_entry(self, widget):
        self.greeting_label = toga.Label(f"{self._name}!, here you can register your training on daily basis")
        # Betöltjük az eddigi adatokat
        self.training_data = load_trainingData()
        # Vissza gomb létrehozása
        back_button = toga.Button('Back', on_press=self.show_welcome_screen)
        #input elemek
        self.training_type = toga.TextInput(placeholder='Training type')
        self.kal_input = toga.TextInput(placeholder='Burnt calories')
        self.time_input = toga.TextInput(placeholder='Time')

        # Dátumválasztó
        self.date_picker = toga.DatePicker()
        # Gomb a beírt adatok mentésére
        self.submit_button = toga.Button('SAVE', on_press=self.handle_submit)


        # Készítsünk el egy elrendezést (box layout)
        self.box = toga.Box(children=[self.greeting_label, back_button, self.training_type, self.kal_input,self.time_input,self.date_picker,self.submit_button],
                            style=Pack(direction='column', padding=20))

        # A box layout-ot rendeljük az ablak közepére
        self.main_window.content = self.box
        pass

    def handle_submit(self, widget):
        training_type = self.training_type.value
        kal = self.kal_input.value
        time = self.time_input.value
        datum = self.date_picker.value

        # Új edzés hozzáadása az adatokhoz
        if datum.isoformat() not in self.training_data:
            self.training_data[datum.isoformat()] = []

        self.training_data[datum.isoformat()].append({
            'Type': training_type,
            'calorie': kal,
            'Time': time,
            'date': datum.strftime('%Y-%m-%d')
        })

        # Adatok mentése
        save_training_data(self.training_data)

        # TextBoxok kiürítése
        self.training_type.value = ''
        self.kal_input.value = ''
        self.time_input.value = ''
    def handle_weight_entry(self, widget):
        # A súly beírásának kezelése
        pass

    def handle_training_statistics(self, widget):
        # Az edzés statisztikák kezelése
        pass

    def handle_weight_statistics(self, widget):
        # A súly statisztikák kezelése
        pass

    def handle_settings(self, widget):
        # A beállítások kezelése
        pass

def main():
    return FitTrackMateApp('FitTrackMate', 'org.fittrackmate')

if __name__ == '__main__':
    app = main()
    app.main_loop()