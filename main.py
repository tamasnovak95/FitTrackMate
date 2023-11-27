import os

import fontTools.feaLib.ast
import toga
from toga.style import Pack
import json
import datetime
import matplotlib.pyplot as plt
from PIL import Image




def save_training_data(data):
    try:
        with open('training_data.json', 'w') as file:
            file.write(json.dumps(data))

    except Exception as e:
        print(f'Error saving data: {e}')
def save_weight_data(data):
    try:
        with open('weight_data.json', 'w') as file:
            file.write(json.dumps(data))

    except Exception as e:
        print(f'Error saving data: {e}')

def load_trainingData():
    if os.path.exists("training_data.json"):
        try:
            with open('training_data.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data
    else:
        # Ha a fájl nem létezik, létrehozzuk és üres adatokkal térítünk vissza
        with open('training_data.json', 'w') as file:
            json.dump({}, file)
        return {}
def load_weight_data():
    if os.path.exists("weight_data.json"):
        try:
            with open('weight_data.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data
    else:
        # Ha a fájl nem létezik, létrehozzuk és üres adatokkal térítünk vissza
        with open('weight_data.json', 'w') as file:
            json.dump({}, file)
        return {}
def convert_date_strings_to_date_objects(data):
    for date, entries in data.items():
        for entry in entries:
            entry_date = entry.get('date', '')
            try:
                entry['date'] = datetime.datetime.strptime(entry_date, '%Y-%m-%d').date()
            except ValueError:
                pass
def convert_to_float(input_string):
    try:
        # Eltávolítjuk a tizedesvesszőt és helyettesítjük ponttal
        input_string = input_string.replace(',', '.')
        result = float(input_string)
        return result
    except ValueError:
        print("Hiba")
        return None
def create_training_chart_and_save():
    # Betöltjük a training_data.json fájlt
    with open('training_data.json', 'r') as file:
        training_data = json.load(file)

    # Szöveg dátumokat dátum objektumokká alakítása
    convert_date_strings_to_date_objects(training_data)

    # Havi összesített kalóriaadatok készítése
    monthly_calories = {}
    for date, entries in training_data.items():
        for entry in entries:
            month = entry['date'].strftime('%Y-%m')
            if month not in monthly_calories:
                monthly_calories[month] = 0
            monthly_calories[month] += entry.get('calorie', 0)

    # Diagram létrehozása
    months = list(monthly_calories.keys())
    calories = list(monthly_calories.values())

    plt.figure(figsize=(8, 6))
    plt.bar(months, calories)
    plt.xlabel('Months')
    plt.ylabel('Calories')
    plt.title('Monthly Calories Burnt')

    # Kép mentése
    image_file = 'chart_training.jpg'
    plt.savefig(image_file, format='jpg')

    # Ellenőrizzük, hogy létezik-e a fájl
    if os.path.exists(image_file):
        # Kép megnyitása PIL segítségével
        img = Image.open(image_file)

        # Kép mentése JPG formátumban
        img.save('saved_chart_image.jpg', 'JPEG')
        print('Chart image saved as saved_chart_image.jpg')
    else:
        print('Error: Image file does not exist')
def create_weight_chart_and_save():
    # Betöltjük a weight_data.json fájlt
    with open('weight_data.json', 'r') as file:
        weight_data = json.load(file)

    # Szöveg dátumokat dátum objektumokká alakítása
    convert_date_strings_to_date_objects(weight_data)

    # Súlyadatok átalakítása float típussá
    for entries in weight_data.values():
        for entry in entries:
            entry['Weight'] = convert_to_float(entry['Weight'])

    # Kezdő és végdátum kinyerése
    dates = [entry['date'] for entries in weight_data.values() for entry in entries]
    start_date = min(dates).strftime('%Y-%m-%d')
    end_date = max(dates).strftime('%Y-%m-%d')

    # Súlyadatok listába gyűjtése
    weights = [entry['Weight'] for entries in weight_data.values() for entry in entries]

    # Diagram létrehozása
    plt.figure(figsize=(8, 6))
    plt.plot(dates, weights)
    plt.xlabel('date')
    plt.ylabel('Weight')
    plt.title(f'Weight Progress from {start_date} to {end_date}')

    # Kép mentése
    image_file = 'chart_weight.jpg'
    plt.savefig(image_file, format='jpg')

    # Ellenőrizzük, hogy létezik-e a fájl
    if os.path.exists(image_file):
        # Kép megnyitása PIL segítségével
        img = Image.open(image_file)

        # Kép mentése JPG formátumban
        img.save('saved_chart_weight.jpg', 'JPEG')
        print('Weight chart image saved as saved_chart_weight.jpg')
    else:
        print('Error: Image file does not exist')
#default_font_size = 10  # Alapértelmezett érték, ha a fájlban nem lenne megadva

class FitTrackMateApp(toga.App):
    SETTINGS_FILE = 'settings.json'

    def __init__(self, formal_name, package_name):
        super().__init__(formal_name, package_name)

        # A név tárolása
        self._name = None

    def load_default_font_size(self):
        default_font_size = 12  # Alapértelmezett érték, ha a fájlban nem lenne megadva

        try:
            if not os.path.exists(self.SETTINGS_FILE):
                self.create_default_settings()

            with open(self.SETTINGS_FILE, 'r') as file:
                data = json.load(file)
                default_font_size = data.get('defaultFontSize')  # A fájlból betöltött érték vagy alapértelmezett érték
        except json.JSONDecodeError:
            print("A settings.json fájl nem megfelelő JSON formátumú.")
        return default_font_size

    def create_default_settings(self):
        default_settings = {'defaultFontSize': 12}  # Alapértelmezett beállítások létrehozása
        with open(self.SETTINGS_FILE, 'w') as file:
            json.dump(default_settings, file, indent=4)

    def change_default_setting(self,new_size):
        try:
            with open(self.SETTINGS_FILE, 'r+') as file:
                data = json.load(file)
                data['defaultFontSize'] = new_size
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                self.default_font_size = new_size  # Frissítjük az aktuális beállítást is
        except json.JSONDecodeError:
            print("A settings.json not valid JSON format.")
        except Exception as e:
            print(f"Some issue happens: {str(e)}")
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

        if not os.path.exists(self.SETTINGS_FILE):
            self.create_default_settings()
        else:
            self.load_default_font_size()
    def ask_for_name(self):
        # Szöveges beviteli mező
        self.name_input = toga.TextInput()

        # Gomb az adat beküldésére és az üzenet kezelésére
        self.submit_button = toga.Button('Submit', on_press=self.submit_name,style=Pack(font_size=self.load_default_font_size()))

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
    def fontsize(self, size):
         return Pack(font_family='Arial', font_size=size)

    def show_welcome_screen(self, widget=None):
        # Üdvözlő üzenet
        default_font_size = self.load_default_font_size()
        self.greeting_label = toga.Label(f"Welcome, {self._name}!",style=Pack(font_size=self.load_default_font_size()))
        button_style = self.fontsize(default_font_size)
        #főmenü gombo
        button1 = toga.Button('Training register',style=button_style, on_press=self.handle_training_entry)
        button2 = toga.Button('Weight register',style=button_style, on_press=self.handle_weight_entry)
        button3 = toga.Button('Training track',style=button_style, on_press=self.handle_training_statistics)
        button4 = toga.Button('Weight track', style=button_style, on_press=self.handle_weight_statistics)
        button5 = toga.Button('Options',style=button_style, on_press=self.handle_settings)
        #Elrendezés
        self.box = toga.Box(children=[self.greeting_label, button1, button2, button3, button4, button5],
                            style=Pack(direction='column', padding=20,))

        # A box layout-ot rendeljük az ablak közepére
        self.main_window.content = self.box
    pass
    # Gomb kezelő függvények
    def handle_training_entry(self, widget):
        self.greeting_label = toga.Label(f"{self._name}!, here you can register your training on daily basis",style=Pack(font_size=self.load_default_font_size()))
        # Betöltjük az eddigi adatokat
        self.training_data = load_trainingData()
        # Vissza gomb létrehozása
        back_button = toga.Button('Back', style=Pack(font_size=self.load_default_font_size()), on_press=self.show_welcome_screen,)
        #input elemek
        self.training_type = toga.TextInput(placeholder='Training type',style=Pack(font_size=self.load_default_font_size()))
        self.kal_input = toga.TextInput(placeholder='Burnt calories',style=Pack(font_size=self.load_default_font_size()))
        self.time_input = toga.TextInput(placeholder='Time',style=Pack(font_size=self.load_default_font_size()))

        # Dátumválasztó
        self.date_picker = toga.DatePicker()
        # Gomb a beírt adatok mentésére
        self.submit_button = toga.Button('SAVE', on_press=self.handle_submit,style=Pack(font_size=self.load_default_font_size()))


        # Készítsünk el egy elrendezést (box layout)
        self.box = toga.Box(children=[self.greeting_label, back_button, self.training_type, self.kal_input,self.time_input,self.date_picker,self.submit_button],
                            style=Pack(direction='column', padding=20))

        # A box layout-ot rendeljük az ablak közepére
        self.main_window.content = self.box
        pass

    def handle_submit(self, widget):
        training_type = self.training_type.value
        kal = int(self.kal_input.value)
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
        self.greeting_label = toga.Label(f"{self._name}!, here you can register your weight on daily basis",style=Pack(font_size=self.load_default_font_size()))
        # Betöltjük az eddigi adatokat
        self.weight_data = load_weight_data()
        # Vissza gomb létrehozása
        back_button = toga.Button('Back', on_press=self.show_welcome_screen,style=Pack(font_size=self.load_default_font_size()))
        # Input elemek
        self.weight_input = toga.TextInput(placeholder='Weight',style=Pack(font_size=self.load_default_font_size()))

        # Dátumválasztó
        self.date_picker = toga.DatePicker()

        # Gomb a beírt adatok mentésére
        self.submit_button = toga.Button('Save', on_press=self.handle_weight_submit,style=Pack(font_size=self.load_default_font_size()))
        self.error_label = toga.Label('Please enter weight in correct format (e.g., 95,0)', style=Pack(font_size=self.load_default_font_size(),color='red'))
        # Készítsünk el egy elrendezést (box layout)
        self.box = toga.Box(
            children=[self.greeting_label, back_button, self.weight_input, self.date_picker, self.submit_button,
                      self.error_label], style=Pack(direction='column', padding=20))


        # A box layout-ot rendeljük az ablak közepére
        self.main_window.content = self.box

        self.weight_input.on_change = self.validate_weight_input
        pass

    def validate_weight_input(self, widget):
        # Ellenőrizze, hogy az érték megfelel-e a kívánt formátumnak (pl. 95,0)
        value = widget.value
        if not value or not value.replace(',', '').replace('.', '').isdigit():
            # Ha nem felel meg a formátumnak, jelenítsen meg egy hibaüzenetet
            self.error_label.text = 'Please enter weight in correct format (e.g., 95,0)'
        else:
            self.error_label.text = ''
            pass  # Hiba kezelése vagy jelzés a felhasználónak
    def handle_weight_submit(self, widget):
        weight = self.weight_input.value
        datum = self.date_picker.value
        if not weight or not weight.replace(',', '').replace('.', '').isdigit():
            # Ha nem felel meg a formátumnak, jelenítsen meg egy hibaüzenetet
            self.error_label.text = 'Data not saved, please correct the format(e.g. 95,0)'
        else:
            self.error_label.text = ''
        # Új súly hozzáadása az adatokhoz
            if datum.isoformat() not in self.weight_data:
                self.weight_data[datum.isoformat()] = []

            self.weight_data[datum.isoformat()].append({
                'Weight': weight,
                'date': datum.strftime('%Y-%m-%d')
        })

        # Adatok mentése
        save_weight_data(self.weight_data)

        # TextBox kiürítése
        self.weight_input.value = ''

    def handle_training_statistics(self, widget):
        # Az edzés statisztikák kezelése

        back_button = toga.Button('Back', on_press=self.handle_back_button,style=Pack(font_size=self.load_default_font_size()))

        # Statisztika megjelenítése

        self.img = toga.ImageView(id='images', image='./chart_training.jpg') #program inditásakor létrehozott image megjelenítése
        # Elrendezés
        self.box = toga.Box(children=[back_button,  self.img],
                            style=Pack(direction='column', padding=20))

        # A box layout-ot rendeljük az ablak közepére
        self.main_window.content = self.box
        pass

    def handle_weight_statistics(self, widget):
        # A súly statisztikák kezelése

        back_button = toga.Button('Back', on_press=self.handle_back_button,style=Pack(font_size=self.load_default_font_size()))

        # Statisztika megjelenítése

        self.img = toga.ImageView(id='images2',image='./chart_weight.jpg')  # program inditásakor létrehozott image megjelenítése
        # Elrendezés
        self.box = toga.Box(children=[back_button, self.img],
                            style=Pack(direction='column', padding=20))

        # A box layout-ot rendeljük az ablak közepére
        self.main_window.content = self.box

        pass

    def handle_back_button(self, widget): #eltávoltítja az img objektumot, így újból megnyithatóvá is teszi
        # A 'self.img' azonosítójú widget eltávolítása a konténerből, ha létezik
        if self.img:
            self.box.remove(self.img)

        self.show_welcome_screen()
    def handle_settings(self, widget):
        # Vissza gomb létrehozása
        back_button = toga.Button('Back', on_press=self.show_welcome_screen,style=Pack(font_size=self.load_default_font_size()))
        # A beállítások kezelése
        # Felhasználó törlése
        # Felhasználó nevének megváltoztatása
        # Betűméret beállítása
        self.FONTSIZE = toga.TextInput(placeholder='Font-Size',style=Pack(font_size=self.load_default_font_size()))
        self.submit_button = toga.Button('Save', on_press=self.submit_settings,style=Pack(font_size=self.load_default_font_size()))

        self.box = toga.Box(
            children=[back_button, self.FONTSIZE, self.submit_button], style=Pack(direction='column', padding=20))
        self.main_window.content = self.box
        pass
    def submit_settings(self, widget):
        try:
            size = int(self.FONTSIZE.value)  # Betűméret konvertálása egész számmá
            if size < 5 or size > 50:
                # Hibaüzenet, ha a beírt érték nem megfelelő
                self.main_window.info_dialog('Error', 'The font size must be at least 5, but no more than 50.')
            else:
                # Betűméret módosítása
                self.change_default_setting(size)
                self.main_window.info_dialog('Success', f'New font size: {size}')
                self.handle_settings(None)
        except ValueError:
            # Hibaüzenet, ha nem számot adott meg a felhasználó
            self.main_window.info_dialog('Error', 'Please enter a valid number.')

        pass
def main():
    create_training_chart_and_save()
    create_weight_chart_and_save()
    return FitTrackMateApp('FitTrackMate', 'org.fittrackmate')

if __name__ == '__main__':
    app = main()
    app.main_loop()