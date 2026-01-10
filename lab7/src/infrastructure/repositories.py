from typing import Dict, Optional
from src.domain.order import Order
from src.application.interfaces import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """In-memory реализация репозитория заказов"""
    
    def __init__(self):
        self._orders: Dict[str, Order] = {}
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)
    
    def save(self, order: Order) -> None:
        self._orders[order.id] = order
    
    def clear(self) -> None:
        """Очистить хранилище (для тестов)"""
        self._orders.clear()