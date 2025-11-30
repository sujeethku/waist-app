import sqlite3

conn = sqlite3.connect("waist_app.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    note TEXT
)
""")

conn.commit()
conn.close()

print("transactions table created successfully!")
print("First expense added successfully!")