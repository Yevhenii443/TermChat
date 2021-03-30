import json
import sqlite3

def insert_into_db(information):
    json_client = open('register.json').read()
    json_object = json.loads(json_client)

    a = (json_object['login'])
    b = (json_object['password'])

    conn = sqlite3.connect('TermChat.db')
    conn.execute('''INSERT INTO TermChat (login, password) VALUES(?, ?)''',
            (a, b))
    
    conn.commit()
    conn.close()

