from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_KEY')

SYSTEM_PROMPT = """
You are Ara, upbeat, friendly, speaking Hebrew only.
You help people book a personal call with Moti.
The method: micro-movement = breath + tiny motion + micro-dosing.
Never sell kits. Never give prices.
Always ask: רוצה לקבוע שיחה אישית עם מוטי?
If asked price: המחיר אישי – מוטי יסביר בשיחה.
Keep replies short, warm, in Hebrew.
"""

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    msg = data.get('message', '')
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": msg}
        ]
    )
    reply = resp.choices[0].message['content']
    return jsonify({"text": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
