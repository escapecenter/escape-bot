from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# טען את המידע מהקובץ
with open("escape_center_data.json", encoding='utf-8') as f:
    data = json.load(f)

@app.route('/')
def index():
    return "Escape Center Bot is running!"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").lower()

    # דוגמה פשוטה – עונים לפי מילות מפתח
    if "מחיר" in user_input:
        return jsonify({"response": "המחירים משתנים לפי חדר וכמות משתתפים – תוכל לפרט?"})
    elif "חדר נרקוס" in user_input or "נרקוס" in user_input:
        return jsonify({"response": data.get("narcos_description", "אין מידע זמין כרגע")})
    else:
        return jsonify({"response": "לא מצאתי תשובה מדויקת – מומלץ להתקשר למתחם בטלפון 050-5255144 כדי לקבל מידע מלא."})

if __name__ == '__main__':
    app.run(debug=True)
