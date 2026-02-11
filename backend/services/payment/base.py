from abc import ABC, abstractmethod
from typing import Dict, Any
from backend.models.payment import Transaction

class PaymentGateway(ABC):
    """All payment providers implement this interface."""
    
    @abstractmethod
    async def create_payment(self, amount: float, currency: str, metadata: Dict) -> Dict:
        """Return payment intent / redirect URL."""
        pass
    
    @abstractmethod
    async def verify_payment(self, payment_id: str) -> Transaction:
        """Verify and record transaction."""
        pass
    
    @abstractmethod
    async def refund(self, transaction_id: str, amount: float = None) -> bool:
        pass
