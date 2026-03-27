from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

@app.route('/')
def home():
    return "🔥 Bot IA activo 🚀"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]

        respuesta = generar_respuesta(user_text)

        send_message(chat_id, respuesta)

    return "ok"

def generar_respuesta(texto_usuario):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": "Eres un experto en ventas de productos 4Life. Responde de forma persuasiva, amigable y clara."},
            {"role": "user", "content": texto_usuario}
        ]
    }

    response = requests.post(OPENAI_URL, headers=headers, json=data)
    result = response.json()

    return result["choices"][0]["message"]["content"]

def send_message(chat_id, text):
    requests.post(TELEGRAM_URL + "sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

if __name__ == "__main__":
    app.run()
