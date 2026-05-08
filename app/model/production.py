"""생산 관련 보조 모델"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from .enums import OrderStatus


@dataclass
class ProductionRecord:
    """생산 이력 기록 보조 모델

    Attributes:
        order_no: 연관 주문 번호
        sample_id: 생산 시료 ID
        started_at: 생산 시작 일시
        completed_at: 생산 완료 일시 (None이면 진행 중)
        produced_quantity: 실제 생산 수량
        status: 생산 상태
    """

    order_no: str
    sample_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    produced_quantity: int = 0
    status: OrderStatus = OrderStatus.PRODUCING
