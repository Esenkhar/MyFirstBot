import sqlite3

def get_db_connection():
    # Create or connect to the database
    conn = sqlite3.connect('bot_database.db')
    # Create cursor for executing SQL-requests
    cursor = conn.cursor()
    # Example of creating the table (id, username, email)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id INTEGER PRIMARY KEY,
                       username TEXT NOT NULL,
                       age INTEGER NOT NULL
                   )
                   ''')
    # Saving changes and closing the connection
    conn.commit()
    return conn
