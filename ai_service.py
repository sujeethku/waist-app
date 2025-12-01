import json
import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

# Load API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paths must be relative to /web/main.py
CATEGORISATION_PROMPT = "../prompts/ai_categorisation_prompt.txt"
INSIGHTS_PROMPT = "../prompts/ai_insights_prompt.txt"


def load_prompt(path):
    """Loads a prompt template from the given path."""
    with open(path, "r") as f:
        return f.read()


# -----------------------------
#  AI CATEGORY PREDICTION
# -----------------------------
def get_category_from_ai(note, amount, date, description=""):
    """Call OpenAI to predict the category."""

    template = load_prompt(CATEGORISATION_PROMPT)

    final_prompt = (
        template
        .replace("<note>", note)
        .replace("<amount>", str(amount))
        .replace("<date>", date)
        .replace("<description>", description or "")
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expense categorisation AI."},
                {"role": "user", "content": final_prompt}
            ]
        )

        ai_text = completion.choices[0].message.content.strip()
        parsed = json.loads(ai_text)

        return parsed.get("category", "Miscellaneous")

    except Exception as e:
        print("AI Error:", e)
        return "Miscellaneous"


# -----------------------------
#  AI INSIGHTS GENERATION
# -----------------------------
def generate_insights(transactions):
    """Generate financial insights from transaction list."""

    template = load_prompt(INSIGHTS_PROMPT)
    formatted_json = json.dumps(transactions, indent=2)

    prompt = template.replace("<TRANSACTIONS>", formatted_json)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a financial insights assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        ai_text = completion.choices[0].message.content.strip()
        return json.loads(ai_text)

    except Exception as e:
        print("AI Insights Error:", e)
        return {
            "summary": "Unable to generate insights.",
            "top_categories": [],
            "highest_transaction": {},
            "recommendation": "Try again later."
        }
