from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/"

@app.route('/')
def home():
    return "🔥 BOT IA VERSION FINAL 🔥"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # 🔥 Validar si no hay datos
    if not data:
        return "ok"

    # 🔥 Procesar mensaje
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")

        respuesta = generar_respuesta(user_text)

        send_message(chat_id, respuesta)

    return "ok"


def generar_respuesta(texto_usuario):
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-4o-mini",
            "input": texto_usuario
        }

        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers=headers,
            json=data
        )

        result = response.json()
        print(result)

        if "output" in result:
            for item in result["output"]:
                for content in item.get("content", []):
                    if "text" in content:
                        return content["text"]

        return "⚠️ IA sin respuesta"

    except Exception as e:
        print(e)
        return "⚠️ Error IA"


def send_message(chat_id, text):
    requests.post(TELEGRAM_URL + "sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
