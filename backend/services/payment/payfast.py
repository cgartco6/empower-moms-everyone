import hashlib
from urllib.parse import urlencode
from backend.services.payment.base import PaymentGateway
from backend.config.settings import settings

class PayFastGateway(PaymentGateway):
    async def create_payment(self, amount: float, currency: str = "ZAR", metadata: Dict = None):
        # PayFast requires MD5 signature
        data = {
            'merchant_id': settings.PAYFAST_MERCHANT_ID,
            'merchant_key': settings.PAYFAST_MERCHANT_KEY,
            'amount': f"{amount:.2f}",
            'item_name': metadata.get('item_name', 'Course'),
            'return_url': settings.PAYFAST_RETURN_URL,
            'cancel_url': settings.PAYFAST_CANCEL_URL,
            'notify_url': settings.PAYFAST_NOTIFY_URL,
        }
        # Generate signature
        param_string = urlencode(sorted(data.items()))
        data['signature'] = hashlib.md5(param_string.encode()).hexdigest()
        
        return {
            "provider": "payfast",
            "redirect_url": f"{settings.PAYFAST_URL}?{urlencode(data)}",
            "payment_id": data.get('m_payment_id', '')
        }
    
    async def verify_payment(self, payment_id: str):
        # Implement ITN verification
        pass
