class FNBEFTGateway(PaymentGateway):
    async def create_payment(self, amount: float, currency: str = "ZAR", metadata: Dict = None):
        # Generate unique payment reference, return bank details
        ref = f"EMP{random.randint(100000,999999)}"
        return {
            "provider": "fnb_eft",
            "bank_account": {
                "bank": "FNB",
                "account_name": "Empower Moms Pty Ltd",
                "account_number": "62855987412",
                "reference": ref
            },
            "amount": amount,
            "expires_at": (datetime.utcnow() + timedelta(days=3)).isoformat()
        }
    
    async def verify_payment(self, payment_id: str):
        # Webhook from FNB (or manual reconciliation)
        pass
