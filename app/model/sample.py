"""시료(Sample) 도메인 모델"""
from dataclasses import dataclass


@dataclass
class Sample:
    """반도체 시료 도메인 객체

    Attributes:
        id: 시료 식별자 ("S-001" 형식)
        name: 시료명
        avg_production_time: 평균 생산 시간 (분/개, 양수)
        yield_rate: 수율 (0 < yield_rate <= 1)
        stock: 재고 수량 (0 이상)
    """

    id: str
    name: str
    avg_production_time: float
    yield_rate: float
    stock: int
