from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.form.get('Body', '').lower()

    resp = MessagingResponse()
    msg = resp.message()

    if "hola" in incoming_msg:
        msg.body("🔥 Bienvenido a 4Life\n\n1️⃣ Salud\n2️⃣ Negocio\n3️⃣ Precios\n4️⃣ Comprar")
    elif incoming_msg == "1":
        msg.body("💚 Mejora tu salud con productos 4Life")
    elif incoming_msg == "2":
        msg.body("💰 Gana dinero desde casa")
    else:
        msg.body("👉 Escribe 'hola' para empezar")

    return str(resp)
