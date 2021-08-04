import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    firstname text, 
    username text, 
    user_id INTEGER, 
    lang text, 
    result text
)
''')
conn.commit()

conn.close()