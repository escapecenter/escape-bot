from flask import Flask, request, jsonify
import requests
import openai
import os
import csv
from io import StringIO

app = Flask(__name__)

# הגדרת מפתח OpenAI מ־Environment Variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# קריאת המידע מתוך Google Sheets (CSV)
def fetch_sheet_data():
    url = "https://docs.google.com/spreadsheets/d/17e13cqXTMQ0aq6-EUpZmgvOKs0sM6OblxM3Wi1V3-FE/export?format=csv"
    response = requests.get(url)
    response.raise_for_status()
    csv_data = StringIO(response.text)
    reader = csv.DictReader(csv_data)
    return list(reader)

@app.route('/')
def index():
    return "Escape Center Bot is running!"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    sheet_data = fetch_sheet_data()

    # בניית הקשר עם כל תוכן הגיליון
    context = "הנה המידע על כל חדרי הבריחה שלנו:\n"
    for row in sheet_data:
        for key, value in row.items():
            context += f"{key}: {value}\n"
        context += "\n"

    prompt = f"""אתה נציג שירות חכם של Escape Center. לקוח שאל אותך:
{user_input}

בהתאם לנתונים שלפניך, תן תשובה מדויקת, מנומסת, מקצועית וללא המצאות.

{context}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response['choices'][0]['message']['content']
    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(debug=True)
