# WAIST – What Am I Spending on Today? 💸

WAIST is a lightweight expense-tracking application built using Python, SQLite, and a simple Flask web interface.  
The goal of the project is to create a practical, usable tool while exploring rapid prototyping, clean data modelling, and AI-assisted (vibe-coding) workflows.

This repo captures the evolution of the app from a terminal-based CLI to a functional web experience.

---

## 🎯 What the app does today

### **Core Features (CLI)**
- Add a new expense (date, amount, category, note)
- Display all expenses in a formatted table
- Delete an expense by ID
- Input validation to prevent errors
- Local SQLite storage (`waist_app.db`)

### **Analysis Features**
- Total spent in the current month  
- Category-wise spending summary  
- Helper functions to support future reporting

### **Early Web App (Flask)**
- Basic login / session workflow  
- HTML templates for:
  - Login
  - Viewing expenses
  - Adding an expense
- Improved UX planned (Phase 4)

---

## 🧱 Tech Stack

- **Python 3.x**
- **SQLite** (local database)
- **Flask** (web app)
- CLI via standard input/output
- Clear separation of concerns:  
  - `db.py` → database interactions  
  - `analysis.py` → reporting & analytics  
  - `app.py` → CLI flow  
  - `main.py` → Flask routes

---

## 📦 Project Structure

```text
waist/
├─ app.py                # CLI entrypoint
├─ main.py               # Flask entrypoint (web UI)
├─ db.py                 # All SQL queries and DB utilities
├─ analysis.py           # Monthly + category analysis
├─ init_db.py            # Creates the initial SQLite schema
├─ populate_db.py        # Adds sample/fake data
├─ templates/
│  ├─ base.html
│  ├─ login.html
│  ├─ expenses.html
│  └─ add_expense.html
└─ waist_app.db          # Database file (auto-created if missing)
