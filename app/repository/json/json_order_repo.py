"""JSON 파일 기반 OrderRepository 구현체"""
import dataclasses
from datetime import datetime
from pathlib import Path
from typing import Union

from app.model.enums import OrderStatus
from app.model.order import Order
from app.repository.order_repository import OrderRepository
from .base_json_repo import BaseJsonRepository


class JsonOrderRepository(BaseJsonRepository, OrderRepository):
    """JSON 파일 기반 주문 Repository 구현체

    저장 규칙:
    - 파일이 없으면 [] 로 자동 생성
    - Atomic Write: .tmp 임시 파일 → os.replace() 원자적 교체
    - OrderStatus Enum은 문자열 값으로 직렬화 ("RESERVED", "PRODUCING" 등)
    - datetime은 ISO 8601 문자열로 직렬화 ("2026-05-08T09:32:15")
    """

    def __init__(self, file_path: Union[str, Path]) -> None:
        BaseJsonRepository.__init__(self, file_path)

    # ------------------------------------------------------------------
    # 직렬화 / 역직렬화 헬퍼
    # ------------------------------------------------------------------

    def _to_dict(self, order: Order) -> dict:
        """Order를 JSON 직렬화 가능한 dict로 변환한다.

        - OrderStatus Enum → 문자열 값
        - datetime → ISO 8601 문자열
        """
        d = dataclasses.asdict(order)
        d["status"] = order.status.value
        d["created_at"] = order.created_at.isoformat()
        return d

    def _from_dict(self, data: dict) -> Order:
        """dict에서 Order 인스턴스를 복원한다.

        - 문자열 → OrderStatus Enum
        - ISO 8601 문자열 → datetime
        """
        return Order(
            order_no=data["order_no"],
            sample_id=data["sample_id"],
            customer_name=data["customer_name"],
            quantity=int(data["quantity"]),
            status=OrderStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
        )

    # ------------------------------------------------------------------
    # BaseRepository CRUD 구현
    # ------------------------------------------------------------------

    def save(self, entity: Order) -> Order:
        """주문을 JSON 파일에 저장한다."""
        records = self._load()
        records.append(self._to_dict(entity))
        self._write_atomic(records)
        return entity

    def find_by_id(self, id: str) -> Order | None:
        """주문 번호로 주문을 조회한다."""
        for record in self._load():
            if record["order_no"] == id:
                return self._from_dict(record)
        return None

    def find_all(self) -> list[Order]:
        """모든 주문을 조회한다."""
        return [self._from_dict(r) for r in self._load()]

    def update(self, entity: Order) -> Order:
        """주문 정보를 업데이트한다."""
        records = self._load()
        for i, record in enumerate(records):
            if record["order_no"] == entity.order_no:
                records[i] = self._to_dict(entity)
                self._write_atomic(records)
                return entity
        raise ValueError(f"Order not found: {entity.order_no}")

    def delete(self, id: str) -> bool:
        """주문 번호로 주문을 삭제한다."""
        records = self._load()
        new_records = [r for r in records if r["order_no"] != id]
        if len(new_records) == len(records):
            return False
        self._write_atomic(new_records)
        return True

    # ------------------------------------------------------------------
    # OrderRepository 특화 메서드 구현
    # ------------------------------------------------------------------

    def find_by_status(self, status: OrderStatus) -> list[Order]:
        """상태별로 주문 목록을 조회한다."""
        return [
            self._from_dict(r)
            for r in self._load()
            if r["status"] == status.value
        ]

    def find_by_sample(self, sample_id: str) -> list[Order]:
        """시료 ID로 주문 목록을 조회한다."""
        return [
            self._from_dict(r)
            for r in self._load()
            if r["sample_id"] == sample_id
        ]

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
        records = self._load()
        for i, record in enumerate(records):
            if record["order_no"] == order_no:
                record["status"] = status.value
                records[i] = record
                self._write_atomic(records)
                return self._from_dict(record)
        raise ValueError(f"Order not found: {order_no}")
