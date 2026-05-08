"""Phase 1 Red: Order dataclass 필드 타입 및 OrderStatus Enum 테스트"""
import pytest
from datetime import datetime
from app.model.order import Order
from app.model.enums import OrderStatus


class TestOrderStatusEnum:
    """OrderStatus Enum 검증 테스트"""

    def test_order_status_has_reserved(self):
        """RESERVED 상태가 존재해야 한다"""
        assert OrderStatus.RESERVED is not None

    def test_order_status_has_rejected(self):
        """REJECTED 상태가 존재해야 한다"""
        assert OrderStatus.REJECTED is not None

    def test_order_status_has_producing(self):
        """PRODUCING 상태가 존재해야 한다"""
        assert OrderStatus.PRODUCING is not None

    def test_order_status_has_confirmed(self):
        """CONFIRMED 상태가 존재해야 한다"""
        assert OrderStatus.CONFIRMED is not None

    def test_order_status_has_release(self):
        """RELEASE 상태가 존재해야 한다"""
        assert OrderStatus.RELEASE is not None

    def test_order_status_values_are_strings(self):
        """OrderStatus 값은 문자열이어야 한다"""
        assert OrderStatus.RESERVED.value == "RESERVED"
        assert OrderStatus.REJECTED.value == "REJECTED"
        assert OrderStatus.PRODUCING.value == "PRODUCING"
        assert OrderStatus.CONFIRMED.value == "CONFIRMED"
        assert OrderStatus.RELEASE.value == "RELEASE"

    def test_order_status_count(self):
        """OrderStatus는 정확히 5개 상태를 가져야 한다"""
        assert len(OrderStatus) == 5

    def test_order_status_from_string(self):
        """문자열로부터 OrderStatus를 생성할 수 있어야 한다"""
        status = OrderStatus("RESERVED")
        assert status == OrderStatus.RESERVED


class TestOrderFields:
    """Order dataclass 필드 타입 및 생성 테스트"""

    def _make_order(self, **kwargs):
        defaults = dict(
            order_no="ORD-20260508-0001",
            sample_id="S-001",
            customer_name="삼성전자 파운드리",
            quantity=200,
            status=OrderStatus.RESERVED,
            created_at=datetime(2026, 5, 8, 9, 32, 15),
        )
        defaults.update(kwargs)
        return Order(**defaults)

    def test_order_creation_with_all_fields(self):
        """모든 필드를 제공해 Order 인스턴스 생성"""
        order = self._make_order()
        assert order.order_no == "ORD-20260508-0001"
        assert order.sample_id == "S-001"
        assert order.customer_name == "삼성전자 파운드리"
        assert order.quantity == 200
        assert order.status == OrderStatus.RESERVED
        assert isinstance(order.created_at, datetime)

    def test_order_no_type(self):
        """order_no 필드는 str 타입이어야 한다"""
        order = self._make_order()
        assert isinstance(order.order_no, str)

    def test_order_sample_id_type(self):
        """sample_id 필드는 str 타입이어야 한다"""
        order = self._make_order()
        assert isinstance(order.sample_id, str)

    def test_order_customer_name_type(self):
        """customer_name 필드는 str 타입이어야 한다"""
        order = self._make_order()
        assert isinstance(order.customer_name, str)

    def test_order_quantity_type(self):
        """quantity 필드는 int 타입이어야 한다"""
        order = self._make_order()
        assert isinstance(order.quantity, int)

    def test_order_status_type(self):
        """status 필드는 OrderStatus 타입이어야 한다"""
        order = self._make_order()
        assert isinstance(order.status, OrderStatus)

    def test_order_created_at_type(self):
        """created_at 필드는 datetime 타입이어야 한다"""
        order = self._make_order()
        assert isinstance(order.created_at, datetime)

    def test_order_is_dataclass(self):
        """Order는 dataclass여야 한다"""
        import dataclasses
        assert dataclasses.is_dataclass(Order)

    def test_order_equality(self):
        """동일한 필드값을 가진 Order 인스턴스는 동등해야 한다"""
        dt = datetime(2026, 5, 8, 9, 32, 15)
        o1 = Order(
            order_no="ORD-20260508-0001",
            sample_id="S-001",
            customer_name="테스트",
            quantity=100,
            status=OrderStatus.RESERVED,
            created_at=dt,
        )
        o2 = Order(
            order_no="ORD-20260508-0001",
            sample_id="S-001",
            customer_name="테스트",
            quantity=100,
            status=OrderStatus.RESERVED,
            created_at=dt,
        )
        assert o1 == o2

    def test_order_all_statuses(self):
        """모든 OrderStatus 값으로 Order를 생성할 수 있어야 한다"""
        for status in OrderStatus:
            order = self._make_order(status=status)
            assert order.status == status
