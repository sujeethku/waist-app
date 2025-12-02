# WAIST — AI-Driven Personal Expense Intelligence System  
*A full-stack, AI-powered financial insights platform built end-to-end to demonstrate technical product execution, AI integration, and system design depth.*

---

## 🎯 Overview

WAIST (What Am I Spending Today?) is a **full-stack AI product** designed and implemented to showcase:

- AI feature integration (OpenAI GPT-4o Mini)
- End-to-end product thinking  
- Technical execution across backend, frontend, and data layers  
- Structured prompting, evals-first thinking, and JSON-safe model usage  
- System design fundamentals applied in a real, working product  
- Shipping high-quality user-facing features in iterative phases  

It combines **LLM-powered categorization**, **AI insight generation**, and a **production-style Flask application** to deliver contextual spending intelligence for users.

This project was built to demonstrate the skills expected of a PM in the AI/ML organisation: problem framing, technical depth, product strategy, and execution rigor.

---

## 🧠 Key Problem This Product Solves

Typical expense trackers provide raw tables.  
Users still ask:

> “Where is my money actually going?”  
> “What patterns am I missing?”  
> “What should I change next month?”  

WAIST automates the cognitive load by leveraging **structured LLM reasoning** to deliver  
**explainable, contextual, personalised insights**.

---

## 🚀 Highlights

### **1. AI Feature Integration with Evals-First Approach**
- Designed deterministic prompts using JSON schema reinforcement  
- Implemented **structured outputs** to eliminate hallucinations  
- Created two AI microservices:
  - `get_category_from_ai` → expense categorization  
  - `generate_insights` → spending intelligence  
- Ensured model robustness by validating, parsing, and sanitizing LLM output  
- Architecture supports model-swapping (OpenAI → Gemini → local models)

---

### **2. Strong System Design Foundations**
WAIST applies expectations around system design:

- Clear separation of responsibilities  
- Scalable logical architecture  
- Stateless web server  
- Persistent SQLite storage (with clear future path to Cloud SQL / Firestore)  
- Modularized AI service layer  

Detailed architecture diagram included below.

---

### **3. User-Centered Product Thinking**
Every feature was built to reduce user friction:

- One-tap AI categorization  
- Insight summaries written at a sixth-grade readability level  
- Actionable recommendations, not just analytics  
- High-contrast UI  
- Zero-conf onboarding possible  

This reflects emphasis on simplicity, clarity, and user empathy.

---

### **4. Iterative Delivery Across Four Phases**
The project followed a structured roadmap:

1. **Phase 1:** CLI prototype → Validate core CRUD flows  
2. **Phase 2:** Persistent DB + analytics  
3. **Phase 3:** UX/UI with Flask + Tailwind  
4. **Phase 4:** AI categorization + insights engine  

Delivered with PM artifacts: requirements, prioritization, RFC, evals-first tests.

---

## 🚀 Running the App Locally

Follow these steps to start the WAIST application on your machine:

### 1. Clone the repository
git clone https://github.com/sujeethku/waist-app
cd waist-app

shell
Copy code

### 2. Install dependencies
pip install -r requirements.txt

yaml
Copy code

### 3. Add your API key  
Create a file named `.env` in the project root:

OPENAI_API_KEY=your-key-here

shell
Copy code

### 4. Initialize the database
python3 init_db.py

kotlin
Copy code

(Optional sample data)
python3 populate_db.py

shell
Copy code

### 5. Start the web application
cd web
python3 main.py

yaml
Copy code

Your app will be available at:

👉 **http://127.0.0.1:5000**

---

## 🏗️ System Architecture

```mermaid
flowchart TD

    subgraph UI["Frontend (HTML + TailwindCSS)"]
        A1["Expense Entry"]
        A2["Transactions Table"]
        A3["AI Insights View"]
    end

    subgraph Backend["Flask Backend"]
        B1["main.py (Routes)"]
        B2["app.py (App Factory)"]
        B3["db.py (DB Layer)"]
        B4["analysis.py"]
        B5["ai_service.py"]
    end

    subgraph DB["SQLite Database"]
        D1["Users"]
        D2["Transactions"]
        D3["Categories"]
    end

    subgraph AI["LLM Service — GPT-4o Mini (Model Swappable)"]
        E1["Expense Categorization"]
        E2["Spending Insights"]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1
    B1 --> B3
    B3 --> D2
    B1 --> B5
    B5 --> E1
    B5 --> E2
    E1 --> B1
    E2 --> B1
