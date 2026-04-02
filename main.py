from fastapi import FastAPI, Request
import mercadopago
import os

app = FastAPI()

sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_ACCESS_TOKEN"))

# "Base de datos" temporal
users = {}

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/create-payment")
async def create_payment(data: dict):
    email = data.get("email")

    preference_data = {
        "items": [
            {
                "title": "Acceso FounderBot",
                "quantity": 1,
                "unit_price": 10000
            }
        ],
        "payer": {
            "email": email
        },
        "external_reference": email,
        "notification_url": "https://pay-per-chat.onrender.com/webhook"
    }

    preference = sdk.preference().create(preference_data)

    return {
        "preference_id": preference["response"]["id"]
    }

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    print("Webhook recibido:", payload)

    payment_id = payload.get("data", {}).get("id")

    if not payment_id:
        return {"status": "ignored"}

    payment = sdk.payment().get(payment_id)
    payment_data = payment["response"]

    print("Payment data:", payment_data)

    if payment_data.get("status") == "approved":
        email = payment_data.get("external_reference")

        if not email:
            email = payment_data.get("payer", {}).get("email")

        if email:
            users[email] = "paid"
            print(f"Usuario {email} marcado como pagado")

    return {"status": "ok"}  # ✅ dentro de la función

@app.get("/check-access")
def check_access(email: str):
    status = users.get(email, "free")
    return {"access": status == "paid"}
