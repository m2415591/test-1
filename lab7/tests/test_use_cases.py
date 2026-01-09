import pytest
from decimal import Decimal
from src.domain.order import Order, OrderLine
from src.domain.money import Money
from src.domain.order_status import OrderStatus
from src.infrastructure.repositories import InMemoryOrderRepository
from src.infrastructure.payment_gateways import FakePaymentGateway
from src.application.use_cases import PayOrderUseCase


class TestPayOrderUseCase:
    """Тесты use-case оплаты заказа"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.repository = InMemoryOrderRepository()
        self.payment_gateway = FakePaymentGateway()
        self.use_case = PayOrderUseCase(self.repository, self.payment_gateway)
        
        # Создаем тестовые данные
        self.order = Order(id="order-1", customer_id="customer-1")
        self.order.add_line("product-1", 2, Money(Decimal('10.00')))
        self.order.add_line("product-2", 1, Money(Decimal('20.00')))
        
        self.repository.save(self.order)
    
    def test_successful_payment(self):
        """Успешная оплата корректного заказа"""
        success, message = self.use_case.execute("order-1")
        
        assert success is True
        assert "paid successfully" in message
        assert "40.00" in message  # 2*10 + 20 = 40
        
        # Проверяем, что заказ сохранен с правильным статусом
        saved_order = self.repository.get_by_id("order-1")
        assert saved_order.status == OrderStatus.PAID
        assert saved_order.is_paid() is True
        
        # Проверяем, что платежный шлюз был вызван
        assert len(self.payment_gateway.charges_log) == 1
        charge = self.payment_gateway.charges_log[0]
        assert charge['order_id'] == "order-1"
        assert charge['amount'].amount == Decimal('40.00')
    
    def test_payment_empty_order_fails(self):
        """Ошибка при оплате пустого заказа"""
        empty_order = Order(id="empty-order", customer_id="customer-1")
        self.repository.save(empty_order)
        
        success, message = self.use_case.execute("empty-order")
        
        assert success is False
        assert "Cannot pay empty order" in message
    
    def test_double_payment_fails(self):
        """Ошибка при повторной оплате"""
        # Первая оплата должна пройти успешно
        self.use_case.execute("order-1")
        
        # Вторая оплата должна завершиться ошибкой
        success, message = self.use_case.execute("order-1")
        
        assert success is False
        assert "already paid" in message or "Order is already paid" in message
    
    def test_cannot_modify_after_payment(self):
        """Невозможность изменения заказа после оплаты"""
        # Оплачиваем заказ
        self.use_case.execute("order-1")
        
        # Пытаемся изменить оплаченный заказ
        paid_order = self.repository.get_by_id("order-1")
        
        with pytest.raises(ValueError, match="Cannot modify paid order"):
            paid_order.add_line("product-3", 1, Money(Decimal('30.00')))
        
        with pytest.raises(ValueError, match="Cannot modify paid order"):
            paid_order.remove_line("product-1")
    
    def test_total_amount_calculation(self):
        """Корректный расчёт итоговой суммы"""
        order = self.repository.get_by_id("order-1")
        
        # Проверяем расчет суммы
        total = order.total_amount
        assert total.amount == Decimal('40.00')  # 2*10 + 20
        
        # Проверяем инвариант: сумма строк равна общей сумме
        assert order.validate_invariants() is True
    
    def test_payment_gateway_failure(self):
        """Обработка ошибки платежного шлюза"""
        # Создаем падающий платежный шлюз
        failing_gateway = FakePaymentGateway(should_succeed=False)
        use_case = PayOrderUseCase(self.repository, failing_gateway)
        
        success, message = use_case.execute("order-1")
        
        assert success is False
        assert "Payment gateway charge failed" in message
        
        # Проверяем, что заказ не был помечен как оплаченный
        order = self.repository.get_by_id("order-1")
        assert order.status == OrderStatus.NEW
    
    def test_order_not_found(self):
        """Обработка несуществующего заказа"""
        success, message = self.use_case.execute("non-existent-order")
        
        assert success is False
        assert "not found" in message


class TestOrderDomain:
    """Тесты доменной модели"""
    
    def test_money_value_object(self):
        """Тест value object Money"""
        money1 = Money(Decimal('10.00'), "USD")
        money2 = Money(Decimal('10.00'), "USD")
        money3 = Money(Decimal('20.00'), "USD")
        
        # Проверка равенства
        assert money1 == money2
        assert money1 != money3
        
        # Проверка сложения
        result = money1 + money2
        assert result.amount == Decimal('20.00')
        
        # Проверка умножения
        result = money1 * 3
        assert result.amount == Decimal('30.00')
    
    def test_order_line_validation(self):
        """Тест валидации строки заказа"""
        with pytest.raises(ValueError, match="Quantity must be positive"):
            OrderLine("product-1", 0, Money(Decimal('10.00')))
    
    def test_money_validation(self):
        """Тест валидации денежной суммы"""
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            Money(Decimal('-10.00'))