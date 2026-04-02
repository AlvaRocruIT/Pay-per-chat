from fastapi import FastAPI, Request
import mercadopago
import os

app = FastAPI()

sdk = mercadopago.SDK(os.getenv(TEST-8106144427069822-040215-cf28994666e69fbba7a6832835aab523-3257438363))

# "Base de datos" temporal
users = {}

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/create-payment")
async def create_payment(data: dict):
    email = data.get("email")

    # Simulación (luego conectas Mercado Pago)
    payment_url = f"link.mercadopago.cl/founderbot={email}"

    return {"payment_url": payment_url}

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

    return {"status": "ok"}

@app.get("/check-access")
def check_access(email: str):
    status = users.get(email, "free")
    return {"access": status == "paid"}
