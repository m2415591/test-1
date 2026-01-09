from typing import Tuple
from domain.order import Order
from domain.money import Money
from .interfaces import OrderRepository, PaymentGateway


class PayOrderUseCase:
    """Use-case для оплаты заказа"""
    
    def __init__(
        self,
        order_repository: OrderRepository,
        payment_gateway: PaymentGateway
    ):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway
    
    def execute(self, order_id: str) -> Tuple[bool, str]:
        """
        Выполнить оплату заказа
        
        Returns:
            Tuple[bool, str]: (успех, сообщение)
        """
        # 1. Загружаем заказ
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return False, f"Order {order_id} not found"
        
        try:
            # 2. Оплачиваем заказ в доменном слое
            order.pay()
            
            # 3. Вызываем платежный шлюз
            success = self.payment_gateway.charge(order_id, order.total_amount)
            if not success:
                return False, "Payment gateway charge failed"
            
            # 4. Сохраняем обновленный заказ
            self.order_repository.save(order)
            
            return True, f"Order {order_id} paid successfully. Amount: {order.total_amount.amount}"
            
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"