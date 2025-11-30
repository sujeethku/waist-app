import sqlite3
import random
import datetime

# Connect to your existing database
conn = sqlite3.connect("waist_app.db")
cursor = conn.cursor()

# Sample data for random generation
categories = ["Food", "Transport", "Bills", "Entertainment", "Groceries", "Health", "Education"]
payment_methods = ["Card", "Cash", "Wallet", "Online"]
descriptions = [
    "Lunch", "Train ticket", "Electricity bill", "Movie night", "Weekly shopping",
    "Gym membership", "Online course", "Coffee", "Doctor visit", "Gift"
]

# Generate 100 random transactions
for _ in range(100):
    date = (datetime.date.today() - datetime.timedelta(days=random.randint(0, 90))).isoformat()
    category = random.choice(categories)
    description = random.choice(descriptions)
    amount = round(random.uniform(5, 200), 2)
    payment_method = random.choice(payment_methods)

    cursor.execute("""
    INSERT INTO transactions (date, category, description, amount, payment_method)
    VALUES (?, ?, ?, ?, ?)
    """, (date, category, description, amount, payment_method))

conn.commit()
conn.close()

print("✅ 100 random transactions added successfully!")
