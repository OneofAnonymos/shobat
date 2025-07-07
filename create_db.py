import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS feelings (
    user_id INTEGER,
    message TEXT,
    date TEXT
)''')
conn.commit()
conn.close()

print("Database created successfully ✅")
