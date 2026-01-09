from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal
from .money import Money
from .order_status import OrderStatus


@dataclass
class OrderLine:
    """Строка заказа - часть агрегата Order"""
    product_id: str
    quantity: int
    unit_price: Money
    
    @property
    def total_price(self) -> Money:
        return self.unit_price * self.quantity
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")


@dataclass
class Order:
    """Агрегат Order - корневая сущность"""
    id: str
    customer_id: str
    status: OrderStatus = OrderStatus.NEW
    lines: List[OrderLine] = field(default_factory=list)
    
    def add_line(self, product_id: str, quantity: int, unit_price: Money) -> None:
        """Добавить строку заказа"""
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        
        self.lines.append(OrderLine(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        ))
    
    def remove_line(self, product_id: str) -> None:
        """Удалить строку заказа"""
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        
        self.lines = [line for line in self.lines if line.product_id != product_id]
    
    @property
    def total_amount(self) -> Money:
        """Рассчитать общую сумму заказа"""
        if not self.lines:
            return Money(Decimal('0'))
        
        total = Money(Decimal('0'))
        for line in self.lines:
            total = total + line.total_price
        return total
    
    def pay(self) -> None:
        """Оплатить заказ"""
        if self.status == OrderStatus.PAID:
            raise ValueError("Order is already paid")
        
        if not self.lines:
            raise ValueError("Cannot pay empty order")
        
        self.status = OrderStatus.PAID
    
    def is_paid(self) -> bool:
        """Проверить, оплачен ли заказ"""
        return self.status == OrderStatus.PAID
    
    def validate_invariants(self) -> bool:
        """Проверить инварианты"""
        # Инвариант 1: сумма строк должна равняться общей сумме
        calculated_total = Money(Decimal('0'))
        for line in self.lines:
            calculated_total = calculated_total + line.total_price
        
        return calculated_total == self.total_amount