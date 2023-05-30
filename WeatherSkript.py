from bs4 import BeautifulSoup
import requests
import sqlite3
import time
import keyboard

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def create_weather_table():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    time TEXT,
                    info TEXT,
                    temperature TEXT,
                    precipitation TEXT,
                    humidity TEXT,
                    wind TEXT
                )''')

    conn.commit()
    conn.close()


def insert_weather_data(city, time, info, temperature, precipitation, humidity, wind):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()

    c.execute('''INSERT INTO weather (city, time, info, temperature, precipitation, humidity, wind)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (city, time, info, temperature, precipitation, humidity, wind))

    conn.commit()
    conn.close()


def scrape_weather_hourly(city_name):
    city_name = city_name.replace(" ", "+")
    try:
        res = requests.get(f'https://www.google.ch/search?q={city_name}+Wetter', headers=headers)
        print("Loading...")

        soup = BeautifulSoup(res.text, 'html.parser')
        location = city_name
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        temperature = soup.select('#wob_tm')[0].getText().strip()
        precipitation = soup.select('#wob_pp')[0].getText().strip()
        humidity = soup.select('#wob_hm')[0].getText().strip()
        wind = soup.select('#wob_ws')[0].getText().strip()

        print("Ort: " + location)
        print("Temperatur: " + temperature + "°C")
        print("Niederschlag: " + precipitation)
        print("Luftfeuchte: " + humidity)
        print("Wind: " + wind)
        print("Zeit: " + time)
        print("Wetter Beschrieb: " + info)

        insert_weather_data(location, time, info, temperature, precipitation, humidity, wind)
        print("Wetterdaten erfolgreich in die Datenbank eingefügt.")

    except:
        print("Please enter a valid city name")


def find_weather(city_name):
    city_name = city_name.replace(" ", "+")
    try:
        res = requests.get(f'https://www.google.ch/search?q={city_name}+Wetter', headers=headers)
        print("Loading...")

        soup = BeautifulSoup(res.text, 'html.parser')
        location = city_name
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        temperature = soup.select('#wob_tm')[0].getText().strip()
        precipitation = soup.select('#wob_pp')[0].getText().strip()
        humidity = soup.select('#wob_hm')[0].getText().strip()
        wind = soup.select('#wob_ws')[0].getText().strip()

        print("Ort: " + location)
        print("Temperatur: " + temperature + "°C")
        print("Niederschlag: " + precipitation)
        print("Luftfeuchte: " + humidity)
        print("Wind: " + wind)
        print("Zeit: " + time)
        print("Wetter Beschrieb: " + info)

        insert_weather_data(location, time, info, temperature, precipitation, humidity, wind)
        print("Wetterdaten erfolgreich in die Datenbank eingefügt.")

    except:
        print("Please enter a valid city name")


def display_all_weather_data():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()

    c.execute("SELECT * FROM weather")
    rows = c.fetchall()

    if len(rows) > 0:
        print("Alle Wetterdaten:")
        for row in rows:
            print("ID:", row[0])
            print("Ort:", row[1])
            print("Zeit:", row[2])
            print("Wetter Beschrieb:", row[3])
            print("Temperatur:", row[4])
            print("Niederschlag:", row[5])
            print("Luftfeuchte:", row[6])
            print("Wind:", row[7])
            print("-----------------------")
    else:
        print("Es sind keine Wetterdaten in der Datenbank vorhanden.")

    conn.close()


def connect_to_database():
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    query = input("Geben Sie Ihre SQL-Abfrage ein (oder 'q' zum Beenden): ")
    while query.lower() != "q":
        try:
            c.execute(query)
            rows = c.fetchall()
            if len(rows) > 0:
                print("Ergebnis:")
                for row in rows:
                    print(row)
            else:
                print("Keine Ergebnisse gefunden.")

        except sqlite3.Error as e:
            print("Fehler bei der Ausführung der Abfrage:", e)

        query = input("Geben Sie Ihre SQL-Abfrage ein (oder 'q' zum Beenden): ")
    conn.close()


def delete_all_entrys ():
    try:
        conn = sqlite3.connect('weather.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM weather")
        conn.commit()
        conn.close()
        print("Alle Einträge wurden erfolgreich gelöscht")
    except sqlite3.Error as e:
        print("Fehler beim Löschen der Einträge.", e)

def main_menu():
    print("Willkommen im Hauptmenü!")
    print("1. Wetterdaten einer Stadt hohlen und in die Datenbank schreiben")
    print("2. Wetterdaten einer Stadt jede Stunde hohlen und in die Datenbank schreiben")
    print("3. Datenbank ausgeben")
    print("4. Mit Datenbank verbinden")
    print("5. Alle Einträge in der Datenbank löschen")
    print("6. Beenden")


def main_loop():
    while True:
        stop = False
        main_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            print("Option 1 ausgewählt.")
            city_name = input("Stadtnamen eingeben: ")
            find_weather(city_name)
            continue

        elif choice == "2":
            print("Option 2 ausgewählt.")
            city_name = input("Stadtnamen eingeben: ")
            scrape_weather_hourly(city_name)
            interval = 3600
            start_time = time.time()
            next_execution = start_time + interval

            while not stop:
                current_time = time.time()
                if current_time >= next_execution:
                    scrape_weather_hourly(city_name)
                    next_execution = current_time + interval
                    continue

                if keyboard.is_pressed("backspace"):
                    print("Wird gestoppt")
                    stop = True

        elif choice == "3":
            print("Option 3 ausgewählt.")
            display_all_weather_data()
            continue

        elif choice == "4":
            print("Verbindung wird aufgebaut!")
            connect_to_database()
            continue

        elif choice == "5":
            print("Verbindung wird aufgebaut!")
            delete_all_entrys()
            continue

        elif choice == "6":
            print("Skript wird beendet!")
            exit()

        else:
            print("Ungültige Eingabe. Bitte eine Zahl zwischen 1 und 5!")
            continue


create_weather_table()
main_loop()
