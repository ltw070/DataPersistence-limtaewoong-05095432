"""Phase 2 Red: SampleRepository 추가 메서드 시그니처 확인 테스트"""
import inspect
import pytest
from app.repository.sample_repository import SampleRepository


class TestSampleRepositoryInterface:
    """SampleRepository 인터페이스 검증 테스트"""

    def test_sample_repository_is_abstract(self):
        """SampleRepository는 직접 인스턴스화할 수 없어야 한다"""
        with pytest.raises(TypeError):
            SampleRepository()

    def test_sample_repository_has_find_by_name_method(self):
        """find_by_name 메서드가 존재해야 한다"""
        assert hasattr(SampleRepository, "find_by_name")
        assert callable(SampleRepository.find_by_name)

    def test_sample_repository_has_update_stock_method(self):
        """update_stock 메서드가 존재해야 한다"""
        assert hasattr(SampleRepository, "update_stock")
        assert callable(SampleRepository.update_stock)

    def test_find_by_name_is_abstract(self):
        """find_by_name은 추상 메서드여야 한다"""
        assert getattr(SampleRepository.find_by_name, "__isabstractmethod__", False)

    def test_update_stock_is_abstract(self):
        """update_stock은 추상 메서드여야 한다"""
        assert getattr(SampleRepository.update_stock, "__isabstractmethod__", False)

    def test_find_by_name_signature(self):
        """find_by_name(keyword: str) 시그니처 확인"""
        sig = inspect.signature(SampleRepository.find_by_name)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "keyword" in params

    def test_update_stock_signature(self):
        """update_stock(sample_id: str, delta: int) 시그니처 확인"""
        sig = inspect.signature(SampleRepository.update_stock)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "sample_id" in params
        assert "delta" in params

    def test_sample_repository_inherits_base_methods(self):
        """SampleRepository는 BaseRepository의 CRUD 메서드를 상속해야 한다"""
        for method in ("save", "find_by_id", "find_all", "update", "delete"):
            assert hasattr(SampleRepository, method)
