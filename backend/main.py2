@app.post("/api/v1/checkout")
async def checkout(cart: CartSchema, payment_method: str):
    # 1. Calculate total
    # 2. Route to appropriate gateway
    gateway_map = {
        "payfast": PayFastGateway(),
        "stripe": StripeGateway(),
        "paypal": PayPalGateway(),
        "crypto_btc": CryptoGateway(coin="BTC"),
        # ...
    }
    gateway = gateway_map[payment_method]
    payment = await gateway.create_payment(
        amount=cart.total,
        currency=cart.currency,
        metadata={"user_id": user.id, "items": cart.items}
    )
    return {"payment": payment}
