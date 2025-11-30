import re

from db import add_transaction, get_all_transactions, get_expenses_by_category, get_expenses_by_date, get_expenses_by_month, get_expenses_min_amount, get_expenses_max_amount, delete_expense, update_expense, get_total_spent_today, get_total_spent_this_month, get_total_by_category, get_highest_spending_category ,get_average_daily_spend_this_month
from tabulate import tabulate
from datetime import datetime

# ---------------------------------------
# COLOR CONSTANTS
# ---------------------------------------
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

def pause():
    input(YELLOW + "\nPress ENTER to continue..." + RESET)

# ---------------------------------------
# VALIDATION FUNCTIONS
# ---------------------------------------

def validate_date(date_str):
    # Step 1: Strict pattern check → must be exactly YYYY-MM-DD
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return False

    # Step 2: Check if it's a real date
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_amount(amount_str):
    try:
        float(amount_str)
        return True
    except ValueError:
        return False

def validate_category(category_str):
    return category_str.strip() != ""

# ---------------------------------------
# TABLE DISPLAY HELPER
# ---------------------------------------

def display_table(rows):
    if not rows:
        print("No matching expenses found.")
        return

    table = []
    for r in rows:
        table.append([r[0], r[1], r[2], r[3], r[4]])

    headers = ["ID", "Date", "Category", "Amount", "Note"]
    print("\n" + tabulate(table, headers, tablefmt="grid"))


# ---------------------------------------
# EXISTING FUNCTIONS (show_menu, handlers)
# ---------------------------------------

def show_menu():
    print(BLUE + "\n====================================" + RESET)
    print(BLUE + "            WAIST - Main Menu       " + RESET)
    print(BLUE + "====================================" + RESET)
    print(CYAN + "1. Add a new expense" + RESET)
    print(CYAN + "2. View expenses" + RESET)
    print(CYAN + "3. Edit an expense" + RESET)
    print(CYAN + "4. Delete an expense" + RESET)
    print(CYAN + "5. View analytics" + RESET)
    print(CYAN + "6. Export to CSV" + RESET)
    print(CYAN + "7. Exit" + RESET)

def handle_add_expense():
    print(BLUE + "\n--- Add a New Expense ---" + RESET)

    # Date validation
    date = input("Date (YYYY-MM-DD): ")
    while not validate_date(date):
        print(RED + "❌ Invalid date. Please enter a valid date (e.g., 2025-11-12)." + RESET)
        pause()
        date = input("Date (YYYY-MM-DD): ")

    # Category validation
    category = input("Category: ")
    while not validate_category(category):
        print(RED + "❌ Category cannot be empty." + RESET)
        pause()
        category = input("Category: ")

    # Amount validation
    amount_str = input("Amount: ")
    while not validate_amount(amount_str):
        print(RED + "❌ Amount must be a number." + RESET)
        pause()
        amount_str = input("Amount: ")

    amount = float(amount_str)

    # Note (optional)
    note = input("Note: ")

    add_transaction(date, category, amount, note)
    print(GREEN + "✅ Expense added successfully!" + RESET)
    pause()

def handle_view_expenses():
    print(BLUE + "\n--- View Expenses ---" + RESET)
    print(CYAN + "1. View All" + RESET)
    print(CYAN + "2. Filters" + RESET)
    print(CYAN + "3. Back" + RESET)

    choice = input("Choose an option (1-3): ").strip()

    if choice == "1":
        rows = get_all_transactions()
        display_table(rows)
        pause()

    elif choice == "2":
        handle_filter_menu()

    elif choice == "3":
        return

    else:
        print(RED + "❌ Invalid choice!" + RESET)
        pause()

def handle_filter_menu():
    while True:
        print(BLUE + "\n--- Filter Expenses ---" + RESET)
        print(CYAN + "1. Filter by Category" + RESET)
        print(CYAN + "2. Filter by Date (YYYY-MM-DD)" + RESET)
        print(CYAN + "3. Filter by Month (YYYY-MM)" + RESET)
        print(CYAN + "4. Filter by Minimum Amount" + RESET)
        print(CYAN + "5. Filter by Maximum Amount" + RESET)
        print(CYAN + "6. Back" + RESET)

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            category = input("Enter category: ").strip()
            rows = get_expenses_by_category(category)
            display_table(rows)
            pause()

        elif choice == "2":
            date = input("Enter date (YYYY-MM-DD): ").strip()
            rows = get_expenses_by_date(date)
            display_table(rows)
            pause()

        elif choice == "3":
            month = input("Enter month (YYYY-MM): ").strip()
            rows = get_expenses_by_month(month)
            display_table(rows)
            pause()

        elif choice == "4":
            try:
                amount = float(input("Enter minimum amount: ").strip())
            except ValueError:
                print(RED + "❌ Invalid amount." + RESET)
                pause()
                continue
            rows = get_expenses_min_amount(amount)
            display_table(rows)
            pause()

        elif choice == "5":
            try:
                amount = float(input("Enter maximum amount: ").strip())
            except ValueError:
                print(RED + "❌ Invalid amount." + RESET)
                pause()
                continue
            rows = get_expenses_max_amount(amount)
            display_table(rows)
            pause()

        elif choice == "6":
            return

        else:
            print(RED + "❌ Invalid choice!" + RESET)
            pause()


def handle_delete_expense():
    print(BLUE + "\n--- Delete Expense ---" + RESET)

    rows = get_all_transactions()

    if not rows:
        print(RED + "❌ No expenses found to delete." + RESET)
        pause()
        return

    display_table(rows)

    print(CYAN + "\nEnter the ID of the expense to delete." + RESET)
    print(CYAN + "Or type 'b' to go back." + RESET)

    user_input = input("Your choice: ").strip().lower()

    if user_input == "b":
        return

    try:
        expense_id = int(user_input)
    except ValueError:
        print(RED + "❌ Invalid ID. Must be a number or 'b'." + RESET)
        pause()
        return

    confirm = input(YELLOW + f"Are you sure you want to delete expense ID {expense_id}? (y/n): " + RESET).lower()

    if confirm == "y":
        delete_expense(expense_id)
        print(GREEN + "✅ Expense deleted successfully!" + RESET)
    else:
        print(YELLOW + "⚠️ Deletion cancelled." + RESET)

    pause()


def handle_edit_expense():
    print(BLUE + "\n--- Edit Expense ---" + RESET)

    rows = get_all_transactions()

    if not rows:
        print(RED + "❌ No expenses found to edit." + RESET)
        pause()
        return

    display_table(rows)

    print(CYAN + "\nEnter the ID of the expense to edit." + RESET)
    print(CYAN + "Or type 'b' to go back." + RESET)

    user_input = input("Your choice: ").strip().lower()

    if user_input == "b":
        return

    try:
        expense_id = int(user_input)
    except ValueError:
        print(RED + "❌ Invalid ID. Must be a number or 'b'." + RESET)
        pause()
        return

    existing = None
    for r in rows:
        if r[0] == expense_id:
            existing = r
            break

    if not existing:
        print(RED + "❌ Expense ID not found." + RESET)
        pause()
        return

    print(YELLOW + "\nPress ENTER to keep the existing value." + RESET)

    new_date = input(f"New date (current: {existing[1]}): ").strip() or existing[1]
    new_category = input(f"New category (current: {existing[2]}): ").strip() or existing[2]

    new_amount_str = input(f"New amount (current: {existing[3]}): ").strip()
    new_amount = float(new_amount_str) if new_amount_str else existing[3]

    new_notes = input(f"New note (current: {existing[4]}): ").strip() or existing[4]

    update_expense(expense_id, new_date, new_category, new_amount, new_notes)

    print(GREEN + "✅ Expense updated successfully!" + RESET)
    pause()


def handle_analytics_menu():
    while True:
        print(BLUE + "\n--- Analytics ---" + RESET)
        print(CYAN + "1. Total Spent Today" + RESET)
        print(CYAN + "2. Total Spent This Month" + RESET)
        print(CYAN + "3. Total by Category" + RESET)
        print(CYAN + "4. Highest Spending Category" + RESET)
        print(CYAN + "5. Average Daily Spend (This Month)" + RESET)
        print(CYAN + "6. Back" + RESET)

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            total = get_total_spent_today()
            print(GREEN + f"\n💰 Total Spent Today: ${total:.2f}" + RESET)
            pause()

        elif choice == "2":
            total = get_total_spent_this_month()
            print(GREEN + f"\n📅 Total Spent This Month: ${total:.2f}" + RESET)
            pause()

        elif choice == "3":
            category = input("Enter category: ").strip()
            total = get_total_by_category(category)
            print(GREEN + f"\n📂 Total Spent in '{category}': ${total:.2f}" + RESET)
            pause()

        elif choice == "4":
            result = get_highest_spending_category()
            if result:
                category, total = result
                print(GREEN + f"\n🏆 Highest Spending Category: '{category}' → ${total:.2f}" + RESET)
            else:
                print(RED + "\nNo expenses recorded yet." + RESET)
            pause()

        elif choice == "5":
            avg = get_average_daily_spend_this_month()
            print(GREEN + f"\n📊 Average Daily Spend (This Month): ${avg:.2f}" + RESET)
            pause()

        elif choice == "6":
            return

        else:
            print(RED + "❌ Invalid choice!" + RESET)
            pause()


# ---------------------------------------
# CSV Download
# ---------------------------------------

import csv

def handle_export_csv():
    print("\n--- Export Expenses to CSV ---")
    pause()

    rows = get_all_transactions()

    if not rows:
        print(RED + "❌ No expenses to export." + RESET)
        pause()
        return

    filename = input("Enter CSV filename (e.g., expenses.csv): ").strip()
    if not filename.endswith(".csv"):
        filename += ".csv"

    try:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Date", "Category", "Amount", "Note"])
            writer.writerows(rows)

        print(GREEN + f"✅ Exported successfully to '{filename}'" + RESET)
        pause()

    except Exception as e:
        print(RED + f"❌ Failed to export CSV:" + RESET, str(e))
        pause()


# ---------------------------------------
# MAIN LOOP
# ---------------------------------------

def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            handle_add_expense()
        elif choice == "2":
            handle_view_expenses()
        elif choice == "3":
            handle_edit_expense()
        elif choice == "4":
            handle_delete_expense()
        elif choice == "5":
            handle_analytics_menu()
        elif choice == "6":
            handle_export_csv()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
