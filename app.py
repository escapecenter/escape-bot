
במחשב שלך, צור תיקייה חדשה בשם למשל escape-bot עם הקבצים הבאים:

📄 app.py – קובץ Flask ראשי:
python
Copy
Edit
from flask import Flask, request, jsonify
import openai
import os
import requests
import csv
from io import StringIO

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# שליפת המידע מה-Google Sheets
def fetch_sheet_data():
    url = "https://docs.google.com/spreadsheets/d/17e13cqXTMQ0aq6-EUpZmgvOKs0sM6OblxM3Wi1V3-FE/edit?usp=sharing"
    response = requests.get(url)
    csv_data = StringIO(response.text)
    reader = csv.DictReader(csv_data)
    return list(reader)

# הפיכת הטבלה לטקסט שהמודל יכול להבין
def convert_data_to_text(data):
    text = ""
    for row in data:
        for key, value in row.items():
            text += f"{key}: {value}\n"
        text += "\n"
    return text

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    data = fetch_sheet_data()
    context = convert_data_to_text(data)

    prompt = f"""השתמש אך ורק במידע הבא כדי לענות על השאלה:
{context}

שאלה:
{user_message}
תשובה:"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "אתה נציג שירות של ESCAPE CENTER. ענה רק לפי המידע שניתן."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message["content"].strip()
    return jsonify({"response": answer})

@app.route('/')
def home():
    return "Escape Bot is running!"

if __name__ == '__main__':
    app.run()
