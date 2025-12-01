from flask import Flask, render_template, request, redirect, url_for, session
import sys
import os

# Allow imports from parent folder (so we can import db.py)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import only what we need at top; others we import inside routes
from db import get_all_transactions

def login_required(route_function):
    """Simple decorator to protect routes that require login."""
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)
    wrapper.__name__ = route_function.__name__
    return wrapper


app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY_CHANGE_THIS"


# ----------------------------
# PUBLIC / AUTH ROUTES
# ----------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    from db import create_user

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            create_user(username, password)
            return redirect(url_for("login"))
        except:
            return "Username already exists"

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    from db import verify_user

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if verify_user(username, password):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid username or password"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form["username"]

        # Check if user exists
        from db import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_exists = cursor.fetchone()
        conn.close()

        if user_exists:
            return redirect(url_for("reset_password", username=username))
        else:
            return "No such user found."

    return render_template("forgot_password.html")


@app.route("/reset-password/<username>", methods=["GET", "POST"])
def reset_password(username):
    from db import update_user_password

    if request.method == "POST":
        new_password = request.form["password"]
        update_user_password(username, new_password)
        return redirect(url_for("login"))

    return render_template("reset_password.html", username=username)


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    from db import verify_user, update_user_password

    username = session["username"]

    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]

        # 1. Verify current password
        if not verify_user(username, current_password):
            return "Current password is incorrect."

        # 2. Update new password
        update_user_password(username, new_password)

        return "Password changed successfully!"

    return render_template("change_password.html", username=username)


# ----------------------------
# PROTECTED APP ROUTES
# ----------------------------

@app.route("/")
@login_required
def home():
    return render_template("index.html")


@app.route("/transactions")
@login_required
def transactions():
    rows = get_all_transactions()
    return render_template("transactions.html", rows=rows)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    if request.method == "POST":
        date = request.form["date"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        note = request.form["note"]

        from db import add_transaction
        # IMPORTANT: match db.py signature (date, category, amount, note)
        add_transaction(date, category, amount, note)

        return redirect(url_for("transactions"))

    return render_template("add_expense.html")


@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit_expense(expense_id):
    from db import get_expense_by_id, update_expense

    if request.method == "POST":
        date = request.form["date"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        note = request.form["note"]

        # match db.py: update_expense(expense_id, amount, category, note, date)
        update_expense(expense_id, amount, category, note, date)
        return redirect(url_for("transactions"))

    # GET → show existing expense
    expense = get_expense_by_id(expense_id)
    return render_template("edit_expense.html", expense=expense)


@app.route("/delete/<int:expense_id>")
@login_required
def delete(expense_id):
    from db import delete_expense
    delete_expense(expense_id)
    return redirect(url_for("transactions"))


@app.route("/analysis")
@login_required
def analysis_page():
    from db import (
        get_total_spent_this_month,
        get_total_spent_today,
        get_highest_spending_category,
        get_average_daily_spend_this_month,
        get_transaction_count,
        get_category_wise_spending
    )

    total_month = get_total_spent_this_month()
    total_today = get_total_spent_today()
    highest = get_highest_spending_category()
    avg_daily = get_average_daily_spend_this_month()
    count = get_transaction_count()
    categories = get_category_wise_spending()

    # Convert to chart-friendly lists
    category_labels = [c[0] for c in categories]
    category_amounts = [c[1] for c in categories]

    return render_template(
        "analysis.html",
        total_month=total_month,
        total_today=total_today,
        highest=highest,
        avg_daily=avg_daily,
        count=count,
        categories=categories,
        category_labels=category_labels,
        category_amounts=category_amounts
    )


@app.route("/export")
@login_required
def export_csv():
    from db import get_all_transactions_for_export
    import csv
    from io import StringIO
    from flask import Response

    rows = get_all_transactions_for_export()

    # Create a CSV in memory
    output = StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["ID", "Date", "Amount", "Category", "Note"])

    # Write rows
    for r in rows:
        writer.writerow(r)

    # Create response
    response = Response(
        output.getvalue(),
        mimetype="text/csv",
    )
    response.headers["Content-Disposition"] = "attachment; filename=waist_export.csv"

    return response

@app.route("/insights")
def insights():
    from ai_service import generate_insights
    transactions = get_all_transactions()

    # Convert DB tuples → JSON dicts
    transactions_list = []
    for row in transactions:
        transactions_list.append({
            "id": row[0],
            "note": row[1],
            "category": row[2],
            "amount": row[3],
            "date": row[4]
        })

    print("DEBUG JSON:", transactions_list)  # TEMP DEBUG

    insights_json = generate_insights(transactions_list)
    return render_template("insights.html", insights=insights_json)


if __name__ == "__main__":
    app.run(debug=True)
