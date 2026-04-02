from fastapi import FastAPI, Request

app = FastAPI()

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

from pydantic import BaseModel

class WebhookData(BaseModel):
    email: str

@app.post("/webhook")
async def webhook(data: WebhookData):
    email = data.email
    users[email] = "paid"
    return {"status": "received"}

@app.get("/check-access")
def check_access(email: str):
    status = users.get(email, "free")
    return {"access": status == "paid"}
