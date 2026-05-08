"""Phase 2 Red: OrderRepository 추가 메서드 시그니처 확인 테스트"""
import inspect
import pytest
from app.repository.order_repository import OrderRepository


class TestOrderRepositoryInterface:
    """OrderRepository 인터페이스 검증 테스트"""

    def test_order_repository_is_abstract(self):
        """OrderRepository는 직접 인스턴스화할 수 없어야 한다"""
        with pytest.raises(TypeError):
            OrderRepository()

    def test_order_repository_has_find_by_status_method(self):
        """find_by_status 메서드가 존재해야 한다"""
        assert hasattr(OrderRepository, "find_by_status")
        assert callable(OrderRepository.find_by_status)

    def test_order_repository_has_find_by_sample_method(self):
        """find_by_sample 메서드가 존재해야 한다"""
        assert hasattr(OrderRepository, "find_by_sample")
        assert callable(OrderRepository.find_by_sample)

    def test_order_repository_has_update_status_method(self):
        """update_status 메서드가 존재해야 한다"""
        assert hasattr(OrderRepository, "update_status")
        assert callable(OrderRepository.update_status)

    def test_find_by_status_is_abstract(self):
        """find_by_status는 추상 메서드여야 한다"""
        assert getattr(OrderRepository.find_by_status, "__isabstractmethod__", False)

    def test_find_by_sample_is_abstract(self):
        """find_by_sample은 추상 메서드여야 한다"""
        assert getattr(OrderRepository.find_by_sample, "__isabstractmethod__", False)

    def test_update_status_is_abstract(self):
        """update_status는 추상 메서드여야 한다"""
        assert getattr(OrderRepository.update_status, "__isabstractmethod__", False)

    def test_find_by_status_signature(self):
        """find_by_status(status: OrderStatus) 시그니처 확인"""
        sig = inspect.signature(OrderRepository.find_by_status)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "status" in params

    def test_find_by_sample_signature(self):
        """find_by_sample(sample_id: str) 시그니처 확인"""
        sig = inspect.signature(OrderRepository.find_by_sample)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "sample_id" in params

    def test_update_status_signature(self):
        """update_status(order_no: str, status: OrderStatus) 시그니처 확인"""
        sig = inspect.signature(OrderRepository.update_status)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "order_no" in params
        assert "status" in params

    def test_order_repository_inherits_base_methods(self):
        """OrderRepository는 BaseRepository의 CRUD 메서드를 상속해야 한다"""
        for method in ("save", "find_by_id", "find_all", "update", "delete"):
            assert hasattr(OrderRepository, method)
