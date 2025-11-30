import sqlite3

DB_NAME = "/Users/sujeethkumartuniki/Desktop/Coding/waist-app/waist_app.db"

def get_total_spent_this_month():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """)

    result = cursor.fetchone()[0]
    conn.close()

    return result if result else 0


def get_category_wise_spending():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        GROUP BY category
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows
