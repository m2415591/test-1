from abc import ABC, abstractmethod
from typing import Optional
from src.domain.order import Order
from src.domain.money import Money


class OrderRepository(ABC):
    """Интерфейс репозитория заказов"""
    
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        """Получить заказ по ID"""
        pass
    
    @abstractmethod
    def save(self, order: Order) -> None:
        """Сохранить заказ"""
        pass


class PaymentGateway(ABC):
    """Интерфейс платежного шлюза"""
    
    @abstractmethod
    def charge(self, order_id: str, amount: Money) -> bool:
        """Списать деньги"""
        pass