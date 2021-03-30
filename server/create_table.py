import sqlite3

def create_db():
    conn = sqlite3.connect('TermChat.db')

    conn.execute('''CREATE TABLE IF NOT EXISTS TermChat (
            login CHAR,
            password CHAR)''')

    conn.close()

