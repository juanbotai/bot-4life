from flask import Flask, request
import requests
import os

# Crear app
app = Flask(__name__)

# Token seguro desde variables de entorno
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ ERROR: No se encontró el BOT_TOKEN")

URL = f"https://api.telegram.org/bot{TOKEN}/"

# Ruta principal
@app.route('/', methods=['GET'])
def home():
    return "🔥 Bot 4Life activo 🚀"

# Webhook de Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "").lower()

        # Respuestas inteligentes
        if "info" in text:
            reply = "🔥 Producto 4Life\n💪 Mejora tu sistema inmune\n¿Quieres más detalles?"
        elif "precio" in text:
            reply = "💰 Precio especial hoy\n👉 Escríbeme para oferta exclusiva"
        elif "comprar" in text:
            reply = "🛒 Excelente decisión\n👉 WhatsApp: https://wa.me/51976339774"
        else:
            reply = "👋 Hola\nEscribe:\n📌 info\n📌 precio\n📌 comprar"

        send_message(chat_id, reply)

    return "ok"

# Función para enviar mensajes
def send_message(chat_id, text):
    requests.post(URL + "sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

# Ejecutar app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
