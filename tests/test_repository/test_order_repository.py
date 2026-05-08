"""Phase 3: JsonOrderRepository PRD 검증 기준 4개 테스트 (tmp_path 사용)"""
import json
import pytest
from datetime import datetime
from pathlib import Path
from app.model.order import Order
from app.model.enums import OrderStatus
from app.repository.json.json_order_repo import JsonOrderRepository

# 공통 픽스처는 conftest.py에서 제공:
# order_repo, order_file_path, order_reserved, order_producing, order_confirmed


class TestOrderSave:
    """test_order_save: RESERVED 상태로 저장 확인"""

    def test_order_save_creates_file(self, order_file_path, order_reserved):
        """save 후 orders.json 파일이 생성되어야 한다"""
        repo = JsonOrderRepository(order_file_path)
        repo.save(order_reserved)
        assert order_file_path.exists()

    def test_order_save_reserved_status(self, order_file_path, order_reserved):
        """RESERVED 상태로 저장되어야 한다"""
        repo = JsonOrderRepository(order_file_path)
        repo.save(order_reserved)

        with open(order_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["status"] == "RESERVED"

    def test_order_save_writes_all_fields(self, order_file_path, order_reserved):
        """모든 필드가 파일에 기록되어야 한다"""
        repo = JsonOrderRepository(order_file_path)
        repo.save(order_reserved)

        with open(order_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        record = data[0]
        assert record["order_no"] == "ORD-20260508-0001"
        assert record["sample_id"] == "S-001"
        assert record["customer_name"] == "삼성전자 파운드리"
        assert record["quantity"] == 200

    def test_order_save_datetime_iso8601(self, order_file_path, order_reserved):
        """created_at이 ISO 8601 형식으로 저장되어야 한다"""
        repo = JsonOrderRepository(order_file_path)
        repo.save(order_reserved)

        with open(order_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        created_at_str = data[0]["created_at"]
        parsed = datetime.fromisoformat(created_at_str)
        assert parsed == datetime(2026, 5, 8, 9, 32, 15)

    def test_order_save_returns_entity(self, order_repo, order_reserved):
        """save는 저장된 엔티티를 반환해야 한다"""
        result = order_repo.save(order_reserved)
        assert result == order_reserved

    def test_order_save_auto_creates_file(self, tmp_path):
        """파일이 없어도 자동 생성되어야 한다"""
        file_path = tmp_path / "new_orders.json"
        assert not file_path.exists()

        repo = JsonOrderRepository(file_path)
        order = Order(
            order_no="ORD-20260508-9999",
            sample_id="S-001",
            customer_name="테스트",
            quantity=10,
            status=OrderStatus.RESERVED,
            created_at=datetime(2026, 5, 8),
        )
        repo.save(order)
        assert file_path.exists()


class TestOrderFindByStatus:
    """test_order_find_by_status: 상태별 필터링 정확성 확인"""

    def test_find_reserved_orders(self, order_repo, order_reserved, order_producing):
        """RESERVED 상태 주문만 필터링해야 한다"""
        order_repo.save(order_reserved)
        order_repo.save(order_producing)

        results = order_repo.find_by_status(OrderStatus.RESERVED)
        assert len(results) == 1
        assert results[0].order_no == "ORD-20260508-0001"
        assert results[0].status == OrderStatus.RESERVED

    def test_find_producing_orders(self, order_repo, order_reserved, order_producing):
        """PRODUCING 상태 주문만 필터링해야 한다"""
        order_repo.save(order_reserved)
        order_repo.save(order_producing)

        results = order_repo.find_by_status(OrderStatus.PRODUCING)
        assert len(results) == 1
        assert results[0].status == OrderStatus.PRODUCING

    def test_find_by_status_empty_result(self, order_repo, order_reserved):
        """해당 상태의 주문이 없으면 빈 목록을 반환해야 한다"""
        order_repo.save(order_reserved)

        results = order_repo.find_by_status(OrderStatus.RELEASE)
        assert results == []

    def test_find_by_sample(self, order_repo, order_reserved, order_producing, order_confirmed):
        """시료 ID로 주문 목록을 조회해야 한다"""
        order_repo.save(order_reserved)
        order_repo.save(order_producing)
        order_repo.save(order_confirmed)

        results = order_repo.find_by_sample("S-001")
        assert len(results) == 2
        order_nos = [o.order_no for o in results]
        assert "ORD-20260508-0001" in order_nos
        assert "ORD-20260508-0002" in order_nos

    def test_find_all_orders(self, order_repo, order_reserved, order_producing, order_confirmed):
        """find_all은 모든 주문을 반환해야 한다"""
        order_repo.save(order_reserved)
        order_repo.save(order_producing)
        order_repo.save(order_confirmed)

        results = order_repo.find_all()
        assert len(results) == 3

    def test_find_by_id_returns_order(self, order_repo, order_reserved):
        """find_by_id로 주문을 조회해야 한다"""
        order_repo.save(order_reserved)
        result = order_repo.find_by_id("ORD-20260508-0001")

        assert result is not None
        assert isinstance(result, Order)
        assert result.status == OrderStatus.RESERVED


class TestOrderUpdateStatus:
    """test_order_update_status: 상태 전이 후 파일에 반영 확인"""

    def test_update_status_reserved_to_producing(self, order_repo, order_reserved):
        """RESERVED → PRODUCING 상태 전이"""
        order_repo.save(order_reserved)
        result = order_repo.update_status("ORD-20260508-0001", OrderStatus.PRODUCING)

        assert result.status == OrderStatus.PRODUCING

    def test_update_status_persisted_to_file(self, order_file_path, order_reserved):
        """상태 변경이 파일에 반영되어야 한다"""
        repo = JsonOrderRepository(order_file_path)
        repo.save(order_reserved)
        repo.update_status("ORD-20260508-0001", OrderStatus.CONFIRMED)

        with open(order_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data[0]["status"] == "CONFIRMED"

    def test_update_status_nonexistent_raises_error(self, order_repo):
        """존재하지 않는 주문의 상태 변경은 ValueError를 발생시켜야 한다"""
        with pytest.raises(ValueError):
            order_repo.update_status("ORD-99999999-9999", OrderStatus.PRODUCING)

    def test_update_status_all_transitions(self, order_repo, order_reserved):
        """모든 상태 전이가 가능해야 한다"""
        order_repo.save(order_reserved)
        transitions = [
            OrderStatus.PRODUCING,
            OrderStatus.CONFIRMED,
            OrderStatus.RELEASE,
        ]
        for status in transitions:
            result = order_repo.update_status("ORD-20260508-0001", status)
            assert result.status == status

    def test_delete_order(self, order_repo, order_reserved):
        """주문 삭제 후 find_by_id는 None을 반환해야 한다"""
        order_repo.save(order_reserved)
        result = order_repo.delete("ORD-20260508-0001")
        assert result is True

        found = order_repo.find_by_id("ORD-20260508-0001")
        assert found is None


class TestOrderPersistence:
    """test_order_persistence: 인스턴스 재생성 후 주문 데이터 유지 확인"""

    def test_data_persists_after_new_instance(self, order_file_path, order_reserved):
        """새 인스턴스를 생성해도 이전에 저장한 데이터가 유지되어야 한다"""
        repo1 = JsonOrderRepository(order_file_path)
        repo1.save(order_reserved)

        # 새 인스턴스로 조회 (영속성 핵심 테스트)
        repo2 = JsonOrderRepository(order_file_path)
        result = repo2.find_by_id("ORD-20260508-0001")

        assert result is not None
        assert result.order_no == "ORD-20260508-0001"
        assert result.status == OrderStatus.RESERVED

    def test_datetime_persists_correctly(self, order_file_path, order_reserved):
        """datetime 필드가 정확하게 영속화되어야 한다"""
        repo1 = JsonOrderRepository(order_file_path)
        repo1.save(order_reserved)

        repo2 = JsonOrderRepository(order_file_path)
        result = repo2.find_by_id("ORD-20260508-0001")

        assert isinstance(result.created_at, datetime)
        assert result.created_at == datetime(2026, 5, 8, 9, 32, 15)

    def test_status_enum_persists_correctly(self, order_file_path, order_reserved):
        """OrderStatus Enum이 정확하게 영속화되어야 한다"""
        repo1 = JsonOrderRepository(order_file_path)
        repo1.save(order_reserved)

        repo2 = JsonOrderRepository(order_file_path)
        result = repo2.find_by_id("ORD-20260508-0001")

        assert isinstance(result.status, OrderStatus)
        assert result.status == OrderStatus.RESERVED

    def test_status_update_persists(self, order_file_path, order_reserved):
        """상태 변경 후 새 인스턴스에서도 변경사항이 유지되어야 한다"""
        repo1 = JsonOrderRepository(order_file_path)
        repo1.save(order_reserved)
        repo1.update_status("ORD-20260508-0001", OrderStatus.PRODUCING)

        repo2 = JsonOrderRepository(order_file_path)
        result = repo2.find_by_id("ORD-20260508-0001")

        assert result.status == OrderStatus.PRODUCING

    def test_multiple_orders_persist(self, order_file_path, order_reserved, order_producing, order_confirmed):
        """여러 주문이 영속성을 유지해야 한다"""
        repo1 = JsonOrderRepository(order_file_path)
        repo1.save(order_reserved)
        repo1.save(order_producing)
        repo1.save(order_confirmed)

        repo2 = JsonOrderRepository(order_file_path)
        all_orders = repo2.find_all()

        assert len(all_orders) == 3
