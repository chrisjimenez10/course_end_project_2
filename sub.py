import sqlite3
from datetime import datetime, timezone # datetime module allows us to Create/Manipulate Date objects -> timezone.utc = We can acquire UTC (UTC = Coordinated Universal Time and each timezone can be UTC+ or UTC-, which is adding or subtracting from the UTC value -> We use UTC timestamps to sort for higher accuracy)
from zoneinfo import ZoneInfo # zoneinfo module gives us access to the ZoneInfo(), which allows us to convert UTC to local
import tzlocal # tzlocal is a dependency module (install from pip library) that detects machine timezone automatically -> tzlocal.get_localzone()
from functools import lru_cache # Using lru_cache() function to "cache" data

# Database file name
DB_NAME: str = 'player_database.db'
# Initial Data - Here, we use a dicitonary to establish COLUMNS (Keys) + ROWS (Values)


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
        player_id, player_name, last_played_utc, last_played_tz, _ = row.fetchone()

        cursor.execute("INSERT INTO player_logins (player_id, login_utc, login_tz) VALUES (?,?,?)", (player_id, utc_now, local_tz))

        cursor.execute("SELECT login_utc from player_logins WHERE player_id = ?", (player_id,))
        list_of_logins = cursor.fetchall()
        conn.commit()
        
        if isinstance(last_played_utc, str):
            last_played_utc = datetime.fromisoformat(last_played_utc.replace('Z', '+00:00'))
        else:
            last_played_utc = last_played_utc
        local_time = local_time_display(last_played_utc)
  

        if len(list_of_logins) > 1:
            print(F"Welcome back {player_name} - Your player id is: {player_id}\nYou last played on {local_time} | {last_played_tz}")
        else:
            print(F"Welcome NEW player {player_name} - Your player id is: {player_id}")

        return player_id


# Decorator function to cache local zone data after hitting the OS system (This helps avoid making mulitple system calls)
"""
* lru = "Least Recently Used". It keeps a cache of function results keyed by the arguments you called it with.
* maxsize=1 means -> Only remember the most recent call. If you call the function again with the same args, it SKIPS running the body and just returns the cached value.
* Every subsequent call after the 1st function call of get_local_tz() ->
1. lru_cache sees get_local_tz() was called with no arguments, and it already has a result cached for ()
2. Skips tzlocal.get_localzone() entirely
3. Returns the same ZoneInfo object instantly
"""
@lru_cache(maxsize=1)
def get_local_tz():
    # 2. Here, we use the ZoneInfo() and tzlocal.get_localzone() to acquire local time zone in the format required to pass into astimezone() -> The data we get when we run tzlocal.get_localzone() is the area time zone the machine is located in like: "America/Chicago", "America/Los_Angeles", or "Asia/Tokyo"
    return ZoneInfo(str(tzlocal.get_localzone()))


def local_time_display(utc_dt: datetime):
    """Function returns local time stamp for readability"""

    # 1. Making sure incoming datetime "utc_dt" is UTC-aware
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)

    # 3. Convert from UTC to local
    local_time = utc_dt.astimezone(get_local_tz())

    # 4. Here, we use the strftime() method to format the string and display the time how we want
    formatted_time: str = local_time.strftime("%m/%d/%Y - %I:%M%p - %Z")
   
    return formatted_time


def player_login_history(player_id, limit=None):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Here, we are implementing the feature of selecting HOW many login records to display via "limit" paramter and default to display ALL login history. Therefore, we are creating a "query" variable that will be used in the actual query command - 1.If no limit is indicated, default is None, therefore only the initialized "query" variable will be passed to the cursor.execute(), which DOES NOT have the LIMIT keyword + 2.If "limit" is not None, then we use the below coniditional logic to concatenate the query string with the LIMIT ?
        query = '''
            SELECT
                players.id,
                players.name,
                players.score,
                player_logins.login_utc,
                player_logins.login_tz
            FROM players JOIN player_logins
            ON players.id = player_logins.player_id
            WHERE players.id = ?
            ORDER BY player_logins.login_utc DESC
        '''
        
        # Here, we create the "params" list to insert into the query command as the variables to be placed inside the ? place holders. The variables we pass into the ? palce holders can be either inside a list or tuple -> We are dynamically adding a concatenated string, so we need to append to the list we initialized (using a list makes sense here). Now, that second list/tuple inside the execute() query command will have the SQL query string command + the tuple/list it needs to replace those ? place holders
        params = [player_id]
        if limit is not None:
            # Here we concatenate the query (ensuring we add the SPACE in the begining here to separate from the last character in the original "query")
            query += ''' LIMIT ?'''
            params.append(limit)

        # cursor.execute() RUNS the query + RETURNS cursor (holding all the data from the query) -> Therefore, we can simply do cursor.fetchall() without storing that into a variable (NOTE: Once we consume/fetch the cursor, the data is no longer there)
        cursor.execute(query, params)
        player_history = cursor.fetchall() # Storing result from cursor to conserve the data

        formatted_history = []
        for (id, name, score, utc_time, zone) in player_history:
            # Here we convert the utc_time fetched from database (returns it as a string) into a datetime object that is UTC (the universal count, not with adding or subtracting based on local time zone -> instructed by +00:00)
            if isinstance(utc_time, str):
                utc_dt = datetime.fromisoformat(utc_time.replace('Z', '+00:00'))
            else:
                utc_dt = utc_time
            # Here, we pass the fetched and converted UTC time stamp from database into our helper function to handle full display conversion
            local_str = local_time_display(utc_dt)
            # Here, we append the entire entry as a tuple using the variables we unpacked from the original fetched tuple into the new list we will display
            formatted_history.append((name, local_str, zone))
        
        print(F"Login History\n{"-"*14}")
        for i, (name, time, area_zone) in enumerate(formatted_history):
            print(F"{len(formatted_history) - i}. {name} | {time} | {area_zone}")
    

def update_score(player_id, score):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE players
        SET score = ?
        WHERE id = ?
        ''', (score, player_id))
        conn.commit()

    