import sqlite3
import pandas as pd
import os
from datetime import datetime, timezone # datetime module allows us to Create/Manipulate Date objects -> timezone.utc = We can acquire UTC (UTC = Coordinated Universal Time and each timezone can be UTC+ or UTC-, which is adding or subtracting from the UTC value -> We use UTC timestamps to sort for higher accuracy)
from zoneinfo import ZoneInfo # zoneinfo module gives us access to the ZoneInfo(), which allows us to convert UTC to local
import tzlocal # tzlocal is a dependency module (install from pip library) that detects machine timezone automatically -> tzlocal.get_localzone()

# Database file name
DB_NAME: str = 'player_database.db'
# Initial Data - Here, we use a dicitonary to establish COLUMNS (Keys) + ROWS (Values)
data = {
    "Path": ["Dark Forest", "Dark Forest", "Mysterious Cave", "Mysterious Cave"],
    "Choices": ["Follow River", "Climb Tree", "Light Torch", "Proceed in Darkness"],
    "Points": [200, 75, 150, 50]
}
# CSV File name -> Will be located in same directory (using relative path)
csv_file = 'game_choices.csv'

# Clear screen function to clean terminal text
clear_screen = lambda: os.system("clear" if os.name == "posix" else "cls")


def init_csv():
    # Here, we use the DataFrame() constructor and pass the "data" variable containing the dictionary as an argument to have Pandas create the Data Frame (Data Frame is a grid-like table with COLUMNS + ROWS)
    df = pd.DataFrame(data)

    # Here, we use use the "os" module and method path.exists() to check if the CSV file has been created already or not
    if not os.path.exists(csv_file):
        df.to_csv(csv_file, index=False)
    else:
        print(F"* {csv_file} * already exists, skipping export...")


def init_db():
    '''This function initializes the database by creating a connection to it and setting up the TABLE + SCHEMA if it doesn't already exist.'''

    # Context Manager to safely handle: CONNECTION to database + CLOSING of database - Creates the database if it doesn't exist
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Create a table and define SCHEMA -> The IF NOT EXISTS clause is used to avoid errors if the table already exists - id is the primary key and will auto-increment, name is a text field that cannot be null, and score is an integer field that also cannot be null
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            score INTEGER NOT NULL DEFAULT 0,
            last_played_utc TEXT,
            last_played_tz TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            login_utc TEXT NOT NULL,
            login_tz TEXT NOT NULL,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
        ''')
        # cursor.execute("DROP TABLE players")
        conn.commit()  # Commit the changes to the database to save the new player record


def login_player(name):
    # Here, we capture the local time zone from the machine (location of user) -> This way, user is not confused when seeing displayed time stamps
    local_tz = str(tzlocal.get_localzone())

    # Here, we capture the UTC timestamp - datetime.now(timezone.utc) RETURNS a datetime object with the UTC timestamp -> We use strftime(), which stands for "string format time", and we pass it format codes to spit out text. We do this to turn the datetime object into a string -> 1.The %Y, %m, %d, %H (24 hour), %M, %S are codes for year, month, day, hour, minute, second (respectively) + 2.The dashes -, spaces, and colons : are just literal characters (SQLite understands this format natively) --> There are other codes like %I, %p, so research if need
    utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(DB_NAME) as conn:
        # Variable to use as tool to execute queries to Data Base
        cursor = conn.cursor()

        # Here, we are using the follow Upsert SQL query to create new player if non-existent or update the last_played columns if player already exists (Using the "ON CONFLICT (name) DO UPDATE SET", we instruct to update with the values we tried to pass if the "name" value provided exists in the table -> We make sure to retain the values we pass with the word "excluded" to set the new values/overriding the previous values) - Using the word RETURNING we instruct SQLite to return the column values for the record/row -> We can return as many of the column values as we want by writing them next to the RETURNING word
        row = cursor.execute('''
        INSERT INTO players (name, last_played_utc, last_played_tz, score)
        VALUES (?,?,?,0)
        ON CONFLICT (name) DO UPDATE SET
            last_played_utc = excluded.last_played_utc,
            last_played_tz = excluded.last_played_tz
        RETURNING id, name, last_played_utc, last_played_tz, score
        ''', (name, utc_now, local_tz))

        # Tuple unpacking to access each column value and pass them into the query that stores player login history into the player_logins table
        player_id, player_name, last_played_utc, last_played_tz, score = row.fetchone()

        cursor.execute("INSERT INTO player_logins (player_id, login_utc, login_tz) VALUES (?,?,?)", (player_id, utc_now, local_tz))

        conn.commit()
        print(player_id, player_name, last_played_utc, last_played_tz, score)

# login_player("Chris")
# login_player("Wendy")
# login_player("Michelle")

def player_login_history(player_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        

def delete_rows_reset_sequence():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM players")  
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='players'")  
        conn.commit()
# delete_rows_reset_sequence()