class CryptoGateway(PaymentGateway):
    async def create_payment(self, amount: float, currency: str, metadata: Dict):
        # Use CoinPayments API
        payload = {
            'amount': amount,
            'currency1': 'USD',   # settle in USD
            'currency2': currency, # e.g. BTC
            'buyer_email': metadata['email'],
            'item_name': metadata['item_name'],
            'ipn_url': settings.COINPAYMENTS_IPN_URL
        }
        headers = {'HMAC': generate_hmac(payload)}
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                'https://www.coinpayments.net/api.php',
                data=payload,
                headers=headers
            )
            return resp.json()  # includes checkout URL
