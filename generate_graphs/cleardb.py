import sqlite3
import os

def clear_database(db_file):
    # Check if the file exists
    if os.path.exists(db_file):
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Execute SQL command to delete all rows from all tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        for table in tables:
            c.execute(f"DELETE FROM {table[0]};")

        # Commit changes and close connection
        conn.commit()
        conn.close()
        print("Database cleared successfully.")
    else:
        print("Database file does not exist.")

# Example usage:
db_file = '/home/teehee2/flurry/flurry/data/camflow.db'
clear_database(db_file)