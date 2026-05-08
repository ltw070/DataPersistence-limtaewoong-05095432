"""주문 상태 Enum 정의"""
from enum import Enum


class OrderStatus(Enum):
    """주문 상태 열거형

    상태 흐름:
        RESERVED -> PRODUCING -> CONFIRMED -> RELEASE
                 -> REJECTED
    """

    RESERVED = "RESERVED"
    REJECTED = "REJECTED"
    PRODUCING = "PRODUCING"
    CONFIRMED = "CONFIRMED"
    RELEASE = "RELEASE"
