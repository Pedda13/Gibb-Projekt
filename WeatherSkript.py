from bs4 import BeautifulSoup
import requests
import sqlite3
import time
import keyboard
import hashlib
import os
import matplotlib.pyplot as plt

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def hash_password(password):
    # Das Passwort vor dem Speichern hashen
    salt = "random_salt"  # Hier kannst du eine zufällige Salz-Zeichenkette verwenden
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed_password


def create_new_user(newuser, password, subfolder):
    db_path = os.path.join(subfolder, "users.db")
    # Mit der Datenbank verbinden
    conn = sqlite3.connect(db_path)  # Passe den Datenbanknamen entsprechend an

    # Passwort hashen
    hashed_password = hash_password(password)

    # Daten in die Datenbank einfügen oder aktualisieren
    conn.execute("INSERT OR REPLACE INTO users (username, password) VALUES (?, ?)", (newuser, hashed_password))

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()


def delete_user(user, subfolder):
    db_path = os.path.join(subfolder, "users.db")
    # Mit der Datenbank verbinden
    conn = sqlite3.connect(db_path)  # Passe den Datenbanknamen entsprechend an
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (user,))
    fetched_user = c.fetchone()
    if not fetched_user:
        print("Benutzer existiert nicht.")
        conn.close()
        return

    # Lösche den Benutzer aus der Datenbank
    c.execute("DELETE FROM users WHERE username=?", (user,))
    conn.commit()
    conn.close()
    os.remove(f"Wetter Datenbanken/weather-{user}.db")


def verify_password(user, password, subfolder):
    db_path = os.path.join(subfolder, "users.db")
    # Mit der Datenbank verbinden
    conn = sqlite3.connect(db_path)  # Passe den Datenbanknamen entsprechend an

    # Das eingegebene Passwort hashen
    hashed_password = hash_password(password)

    # Das gehashte Passwort aus der Datenbank abrufen
    cursor = conn.execute("SELECT password FROM users WHERE username = ?", (user,))
    result = cursor.fetchone()

    # Verbindung schließen
    conn.close()

    # Das eingegebene Passwort mit dem in der Datenbank gespeicherten Passwort vergleichen
    if result is not None:
        stored_password = result[0]
        if hashed_password == stored_password:
            return True

    return False


def create_weather_table(user, subfolder):
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    db_path = os.path.join(subfolder, f'weather-{user}.db')
    conn = sqlite3.connect(db_path)
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


def create_users_table(subfolder):
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    db_path = os.path.join(subfolder, "users.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Tabelle für Benutzer erstellen
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL)''')

    conn.commit()
    conn.close()


def insert_weather_data(city, time, info, temperature, precipitation, humidity, wind, user, subfolder):
    db_path = os.path.join(subfolder, f'weather-{user}.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''INSERT INTO weather (city, time, info, temperature, precipitation, humidity, wind)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (city, time, info, temperature, precipitation, humidity, wind))

    conn.commit()
    conn.close()


def scrape_weather_hourly(city_name, user):
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

        insert_weather_data(location, time, info, temperature, precipitation, humidity, wind, user, "Wetter Datenbanken")
        print("Wetterdaten erfolgreich in die Datenbank eingefügt.")

    except:
        print("Please enter a valid city name")


def find_weather(city_name, user):
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

        insert_weather_data(location, time, info, temperature, precipitation, humidity, wind, user, "Wetter Datenbanken")
        print("Wetterdaten erfolgreich in die Datenbank eingefügt.")

    except:
        print("Please enter a valid city name")


def display_all_weather_data(user, subfolder):
    db_path = os.path.join(subfolder, f'weather-{user}.db')
    conn = sqlite3.connect(db_path)
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


def display_all_users():
    db_path = os.path.join("User Datenbank", "users.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("SELECT username FROM users")
        rows = c.fetchall()
        if len(rows) > 0:
            print("Ergebnis:")
            for row in rows:
                print(row)
        else:
            print("Keine Ergebnisse gefunden.")

    except sqlite3.Error as e:
        print("Fehler bei der Ausführung der Abfrage:", e)


def connect_to_weather_database(user, subfolder):
    db_path = os.path.join(subfolder, f'weather-{user}.db')
    conn = sqlite3.connect(db_path)
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


def show_graphs (city, subfolder, user):
    db_path = os.path.join(subfolder, f'weather-{user}.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM weather WHERE city=?", (city,))
    rows = c.fetchall()

    if len(rows) > 0:
        temperatures = [float(row[4]) for row in rows]  # Liste der Temperaturen für die Stadt extrahieren
        timestamps = [row[2] for row in rows]  # Liste der Zeitstempel für die Stadt extrahieren

        plt.plot(timestamps, temperatures)
        plt.xlabel('Zeit')
        plt.ylabel('Temperatur (°C)')
        plt.title('Temperaturverlauf für ' + city)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Es sind keine Wetterdaten für", city, "in der Datenbank vorhanden.")

    conn.close()


def delete_all_entrys (user, subfolder):
    try:
        db_path = os.path.join(subfolder, f'weather-{user}.db')
        conn = sqlite3.connect(db_path)
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
    print("6. Temperatur Graphik einer Stadt anzeigen")
    print("7. Beenden")


def admin_menu():
    print("Willkommen im Admin-Hauptmenü!")
    print("1. Alle Benutzer anzeigen")
    print("2. Neuen Benutzer erstellen")
    print("3. Vorhandenen Benutzer löschen")
    print("4. Ausgewählte Datenbank ausgeben")
    print("5. Mit ausgewählter Datenbank verbinden")
    print("6. Alle Einträge der ausgewählten Datenbank löschen")
    print("7. Andere Datenbank auswählen")
    print("8. Beenden")


def admin_loop():
    folder_path = 'Wetter Datenbanken'  # Passe den Pfad zum gewünschten Ordner an
    # Alle Dateien im Ordner anzeigen
    files = os.listdir(folder_path)
    # Durch die Liste der Dateien iterieren und anzeigen
    for file in files:
        print(file)
    print("Bitte Wähle zuerst eine Datenbank aus")
    database_choice = input("Bitte nur den Namen des Users eingeben (Falls keine vorhanden ist einfach leer lassen): ")
    while True:
        admin_menu()
        choice = input("Auswahl eingeben (1-8): ")

        if choice == "1":
            print("Option 1 ausgewählt.")
            display_all_users()
            continue

        elif choice == "2":
            print("Option 2 ausgewählt.")
            newuser = input("Benutzername eingeben")
            password = input("Password eingeben")
            create_new_user(newuser, password, "User Datenbank")
            create_weather_table(newuser, "Wetter Datenbanken")
            continue

        elif choice == "3":
            print("Verbindung wird aufgebaut!")
            delete_user(database_choice, "User Datenbank")
            continue

        elif choice == "4":
            print("Verbindung wird aufgebaut!")
            display_all_weather_data(database_choice, "Wetter Datenbanken")
            continue

        elif choice == "5":
            print("Verbindung wird aufgebaut!")
            connect_to_weather_database(database_choice, "Wetter Datenbanken")
            continue

        elif choice == "6":
            print("Verbindung wird aufgebaut!")
            delete_all_entrys(database_choice, "Wetter Datenbanken")

        elif choice == "7":
            print("Option 7 ausgewählt.")
            admin_loop()

        elif choice == "8":
            print("Skript wird beendet!")
            exit()

        else:
            print("Ungültige Eingabe. Bitte eine Zahl zwischen 1 und 5!")
            continue


def login_menu():
    administrator = False
    print("Login")
    print("Bitte gebe den Benutzernamen ein:")
    global username
    username = input("Benutzername: ")
    print("Bitte gebe das Passwort ein:")
    password = input("Passwort: ")
    if not verify_password(username, password, "User Datenbank"):
        print("Falscher Benutzername oder Passwort")
        login_menu()
    else:
        if username.lower() == "admin":
            administrator = True
            return administrator
        else:
            return administrator


def main_loop():
    create_users_table("User Datenbank")
    if login_menu():
        admin_loop()
        exit()
    else:
        create_weather_table(username, "Wetter Datenbanken")
    while True:
        stop = False
        main_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            print("Option 1 ausgewählt.")
            city_name = input("Stadtnamen eingeben: ")
            find_weather(city_name, username)
            continue

        elif choice == "2":
            print("Option 2 ausgewählt.")
            city_name = input("Stadtnamen eingeben: ")
            scrape_weather_hourly(city_name, username)
            interval = 500
            start_time = time.time()
            next_execution = start_time + interval

            while not stop:
                current_time = time.time()
                if current_time >= next_execution:
                    scrape_weather_hourly(city_name, username)
                    next_execution = current_time + interval
                    continue

                if keyboard.is_pressed("backspace"):
                    print("Wird gestoppt")
                    stop = True

        elif choice == "3":
            print("Option 3 ausgewählt.")
            display_all_weather_data(username, "Wetter Datenbanken")
            continue

        elif choice == "4":
            print("Verbindung wird aufgebaut!")
            connect_to_weather_database(username, "Wetter Datenbanken")
            continue

        elif choice == "5":
            print("Verbindung wird aufgebaut!")
            delete_all_entrys(username, "Wetter Datenbanken")
            continue

        elif choice == "6":
            print("Option 6 ausgewählt.")
            city_name = input("Stadtname eingeben: ")
            show_graphs(city_name, "Wetter Datenbanken", username)
            continue

        elif choice == "7":
            print("Skript wird beendet!")
            exit()

        else:
            print("Ungültige Eingabe. Bitte eine Zahl zwischen 1 und 7!")
            continue


main_loop()