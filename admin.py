import sqlite3
from sub import DB_NAME

PLAYERS_TABLE = "players"
PLAYER_LOGINS_TABLE = "player_logins"

def delete_rows_reset_sequence(table):
    """This function resets table dynamically including all rows and reseting the auto-increment sequence"""

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(F"DELETE FROM {table}") # NOTE: We CANNOT use placeholders here because we are referencing a table name -> Place holders "?" are only for VALUES - Therefore, we can simply use an F string
        cursor.execute(F"DELETE FROM sqlite_sequence WHERE name=?", (table,)) # Here, we CAN use a place holder because we are passing the table name as a VALUE
        conn.commit()

if __name__ == "__main__":
    delete_rows_reset_sequence(PLAYERS_TABLE)
    delete_rows_reset_sequence(PLAYER_LOGINS_TABLE)