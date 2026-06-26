import sqlite3
import pandas as pd
import os

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
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
        ''')
        conn.commit()  # Commit the changes to the database to save the new player record

# Clear screen function to clean terminal text
clear_screen = lambda: os.system("clear" if os.name == "posix" else "cls")
