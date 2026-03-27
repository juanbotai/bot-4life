from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8655577511:AAFJkIgTZgQ4TMb2IDmOzUbTjdd0T_uq3Yw"
URL = f"https://api.telegram.org/bot{TOKEN}/"

@app.route('/', methods=['GET'])
def home():
    return "🔥 Bot 4Life activo 🚀"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].lower()

        if "info" in text:
            reply = "🔥 Producto 4Life mejora tu sistema inmune"
        elif "precio" in text:
            reply = "💰 Precio especial ¿quieres comprar?"
        else:
            reply = "👋 Escribe: info o precio"

        send_message(chat_id, reply)

    return "ok"

def send_message(chat_id, text):
    requests.post(URL + "sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

if __name__ == "__main__":
    app.run()
