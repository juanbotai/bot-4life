from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


@app.route('/')
def home():
    return "🔥 BOT IA 4LIFE ACTIVO 🔥"


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return "ok"

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "").lower()

        respuesta = manejar_mensaje(user_text)

        send_message(chat_id, respuesta)

    return "ok"


# 🔥 MENÚ INTELIGENTE + IA
def manejar_mensaje(texto):
    
    # MENÚ PRINCIPAL
    if "hola" in texto:
        return (
            "🔥 BIENVENIDO AL SISTEMA 4LIFE 💪\n\n"
            "💚 Mejora tu salud\n"
            "⚡ Aumenta tu energía\n"
            "💰 Genera ingresos\n\n"
            "👉 Elige una opción:\n"
            "1️⃣ Salud\n"
            "2️⃣ Negocio\n"
            "3️⃣ Precios\n"
            "4️⃣ Comprar"
        )

    elif texto == "1":
        return "💚 Nuestros productos fortalecen tu sistema inmune y mejoran tu salud 🔥"

    elif texto == "2":
        return "💰 Con 4Life puedes generar ingresos desde casa con tu celular 🚀"

    elif texto == "3":
        return "📊 Te enviaré la lista de precios actualizada 👍"

    elif texto == "4":
        return "🛒 Para comprar envía:\nNombre - Ciudad - Producto"

    # 🔥 SI NO ES MENÚ → USA IA
    else:
        return generar_respuesta_ia(texto)


# 🔥 IA MEJORADA
def generar_respuesta_ia(texto_usuario):
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-4o-mini",
            "input": f"Eres un asesor de ventas de 4Life. Responde de forma clara, corta y convincente: {texto_usuario}"
        }

        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers=headers,
            json=data,
            timeout=10
        )

        result = response.json()

        if "output" in result:
            for item in result["output"]:
                for content in item.get("content", []):
                    if "text" in content:
                        return content["text"]

        return "⚠️ No pude responder eso, escribe 'hola' para ver el menú"

    except Exception as e:
        print("Error IA:", e)
        return "⚠️ Hubo un problema, intenta nuevamente"


# 🔥 ENVÍO SEGURO
def send_message(chat_id, text):
    try:
        requests.post(TELEGRAM_URL, json={
            "chat_id": chat_id,
            "text": text
        }, timeout=5)
    except Exception as e:
        print("Error enviando mensaje:", e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
