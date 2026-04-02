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
    payment_url = f"https://fake-payment.com/pay?email={email}"

    return {"payment_url": payment_url}

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    email = payload.get("email")

    if email:
        users[email] = "paid"

    return {"status": "received"}

@app.get("/check-access")
def check_access(email: str):
    status = users.get(email, "free")
    return {"access": status == "paid"}
