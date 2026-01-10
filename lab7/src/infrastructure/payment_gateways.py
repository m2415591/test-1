from src.domain.money import Money
from src.application.interfaces import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    """Фейковый платежный шлюз для тестирования"""
    
    def __init__(self, should_succeed: bool = True):
        self.should_succeed = should_succeed
        self.charges_log = []
    
    def charge(self, order_id: str, amount: Money) -> bool:
        """Имитирует списание денег"""
        self.charges_log.append({
            'order_id': order_id,
            'amount': amount
        })
        
        if not self.should_succeed:
            return False
        
        # Здесь могла бы быть реальная интеграция с платежной системой
        print(f"[FakePaymentGateway] Charged {amount.amount} {amount.currency} for order {order_id}")
        return True