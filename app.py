from flask import Flask, request, jsonify
import requests
import csv
import openai
import os
from io import StringIO

app = Flask(__name__)

# הגדרת המפתח של OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# שליפת המידע מהטבלה (Google Sheets)
def fetch_sheet_data():
    url = "https://docs.google.com/spreadsheets/d/17e13cqXTMQ0aq6-EUpZmgvOKs0sM6OblxM3Wi1V3-FE/export?format=csv"
    response = requests.get(url)
    response.raise_for_status()
    csv_data = StringIO(response.text)
    reader = csv.DictReader(csv_data)
    return list(reader)

# הפיכת הטבלה לטקסט שהבוט יבין
def convert_data_to_text(data):
    text = ""
    for row in data:
        for key, value in row.items():
            text += f"{key}: {value}\n"
        text += "\n"
    return text

@app.route('/')
def index():
    return "Escape Center Bot with GPT is running!"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").strip()
    sheet_data = fetch_sheet_data()
    context_text = convert_data_to_text(sheet_data)

    prompt = f"""השתמש רק במידע הבא על חדרי בריחה כדי לענות לשאלה.
המידע:
{context_text}

שאלה:
{user_input}

תשובה:"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "אתה עוזר אדיב שעונה רק מתוך מידע שניתן לך על חדרי בריחה."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )

        reply = completion.choices[0].message["content"].strip()
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"שגיאה: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
