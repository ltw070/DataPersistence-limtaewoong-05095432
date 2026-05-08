"""주문(Order) 도메인 모델"""
from dataclasses import dataclass
from datetime import datetime
from .enums import OrderStatus


@dataclass
class Order:
    """생산 주문 도메인 객체

    Attributes:
        order_no: 주문 번호 ("ORD-YYYYMMDD-XXXX" 형식)
        sample_id: 대상 시료 ID
        customer_name: 고객명
        quantity: 주문 수량 (양수)
        status: 주문 상태
        created_at: 주문 생성 일시
    """

    order_no: str
    sample_id: str
    customer_name: str
    quantity: int
    status: OrderStatus
    created_at: datetime
