import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Use your actual DB file
DB_NAME = "/Users/sujeethkumartuniki/Desktop/Coding/waist-app/waist_app.db"


def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_NAME)


# ----------------------------
# TRANSACTIONS CRUD FUNCTIONS
# ----------------------------

def add_transaction(date, category, amount, note):
    """Insert a new transaction. Column name is 'note' (not 'notes')."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (date, category, amount, note)
        VALUES (?, ?, ?, ?)
    """, (date, category, amount, note))
    conn.commit()
    conn.close()


def get_all_transactions():
    """Return all transactions ordered by date DESC.

    Order of columns must match how templates use row indices:
    id, date, amount, category, note
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, category, note
        FROM transactions
        ORDER BY date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expenses_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, category, note
        FROM transactions
        WHERE category = ?
        ORDER BY date DESC
    """, (category,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expenses_by_date(date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, category, note
        FROM transactions
        WHERE date = ?
        ORDER BY date DESC
    """, (date,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expenses_by_month(month):
    """month in format 'YYYY-MM'."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, category, note
        FROM transactions
        WHERE substr(date, 1, 7) = ?
        ORDER BY date DESC
    """, (month,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expenses_min_amount(min_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, category, note
        FROM transactions
        WHERE amount >= ?
        ORDER BY amount DESC
    """, (min_amount,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expenses_max_amount(max_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, category, note
        FROM transactions
        WHERE amount <= ?
        ORDER BY amount ASC
    """, (max_amount,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM transactions
        WHERE id = ?
    """, (expense_id,))
    conn.commit()
    conn.close()


def get_expense_by_id(expense_id):
    """Return a single expense row by id: (id, date, amount, category, note)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, category, note
        FROM transactions
        WHERE id = ?
    """, (expense_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def update_expense(expense_id, amount, category, note, date):
    """Update an expense. Order of args must match how main.py calls it."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions
        SET amount = ?, category = ?, note = ?, date = ?
        WHERE id = ?
    """, (amount, category, note, date, expense_id))
    conn.commit()
    conn.close()


# ----------------------------
# ANALYSIS FUNCTIONS
# ----------------------------

def get_total_spent_today():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE date = DATE('now')
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result or 0


def get_total_spent_this_month():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """)
    result = cursor.fetchone()[0]
    conn.close()
    return result or 0


def get_total_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE category = ?
    """, (category,))
    result = cursor.fetchone()[0]
    conn.close()
    return result or 0


def get_highest_spending_category():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """)
    result = cursor.fetchone()
    conn.close()
    return result  # (category, total) or None


def get_average_daily_spend_this_month():
    import calendar

    conn = get_connection()
    cursor = conn.cursor()

    # Total for this month
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """)
    total = cursor.fetchone()[0] or 0

    # Days in current month
    cursor.execute("SELECT strftime('%Y', 'now'), strftime('%m', 'now')")
    year, month = cursor.fetchone()
    year = int(year)
    month = int(month)
    days_in_month = calendar.monthrange(year, month)[1]

    conn.close()
    return total / days_in_month if days_in_month > 0 else 0


def get_transaction_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    result = cursor.fetchone()[0]
    conn.close()
    return result or 0


def get_category_wise_spending():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_transactions_for_export():
    """Used by /export route. Keep same order as UI expects."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, category, note
        FROM transactions
        ORDER BY date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


# ----------------------------
# AUTH FUNCTIONS (users table)
# ----------------------------

def create_user(username, password):
    """Create a new user with a hashed password."""
    conn = get_connection()
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)

    cursor.execute("""
        INSERT INTO users (username, password)
        VALUES (?, ?)
    """, (username, hashed_password))

    conn.commit()
    conn.close()


def verify_user(username, password):
    """Check if username exists and password is correct."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False

    hashed_password = row[0]
    return check_password_hash(hashed_password, password)


def update_user_password(username, new_password):
    """Update password for a user, with hashing."""
    conn = get_connection()
    cursor = conn.cursor()
    hashed = generate_password_hash(new_password)
    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE username = ?
    """, (hashed, username))
    conn.commit()
    conn.close()
