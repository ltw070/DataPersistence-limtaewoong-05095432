"""OrderRepository 추상 인터페이스"""
from abc import abstractmethod
from app.model.order import Order
from app.model.enums import OrderStatus
from .base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """주문(Order) 전용 Repository 인터페이스

    BaseRepository의 CRUD 메서드에 더해 주문 특화 조회/수정 메서드를 정의한다.
    """

    @abstractmethod
    def find_by_status(self, status: OrderStatus) -> list[Order]:
        """상태별로 주문 목록을 조회한다.

        Args:
            status: 조회할 주문 상태

        Returns:
            해당 상태의 주문 목록
        """
        ...

    @abstractmethod
    def find_by_sample(self, sample_id: str) -> list[Order]:
        """시료 ID로 주문 목록을 조회한다.

        Args:
            sample_id: 조회할 시료의 ID

        Returns:
            해당 시료와 연관된 주문 목록
        """
        ...

    @abstractmethod
    def update_status(self, order_no: str, status: OrderStatus) -> Order:
        """주문 상태를 변경한다.

        Args:
            order_no: 상태를 변경할 주문 번호
            status: 새로운 주문 상태

        Returns:
            업데이트된 주문

        Raises:
            ValueError: 주문이 존재하지 않는 경우
        """
        ...
