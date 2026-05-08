"""Phase 2 Red: BaseRepository 추상 메서드 존재 확인 테스트"""
import inspect
import pytest
from app.repository.base_repository import BaseRepository


class TestBaseRepositoryInterface:
    """BaseRepository 추상 인터페이스 검증 테스트"""

    def test_base_repository_is_abstract(self):
        """BaseRepository는 직접 인스턴스화할 수 없어야 한다"""
        with pytest.raises(TypeError):
            BaseRepository()

    def test_base_repository_has_save_method(self):
        """save 추상 메서드가 존재해야 한다"""
        assert hasattr(BaseRepository, "save")
        assert callable(BaseRepository.save)

    def test_base_repository_has_find_by_id_method(self):
        """find_by_id 추상 메서드가 존재해야 한다"""
        assert hasattr(BaseRepository, "find_by_id")
        assert callable(BaseRepository.find_by_id)

    def test_base_repository_has_find_all_method(self):
        """find_all 추상 메서드가 존재해야 한다"""
        assert hasattr(BaseRepository, "find_all")
        assert callable(BaseRepository.find_all)

    def test_base_repository_has_update_method(self):
        """update 추상 메서드가 존재해야 한다"""
        assert hasattr(BaseRepository, "update")
        assert callable(BaseRepository.update)

    def test_base_repository_has_delete_method(self):
        """delete 추상 메서드가 존재해야 한다"""
        assert hasattr(BaseRepository, "delete")
        assert callable(BaseRepository.delete)

    def test_save_is_abstract(self):
        """save는 추상 메서드여야 한다"""
        assert getattr(BaseRepository.save, "__isabstractmethod__", False)

    def test_find_by_id_is_abstract(self):
        """find_by_id는 추상 메서드여야 한다"""
        assert getattr(BaseRepository.find_by_id, "__isabstractmethod__", False)

    def test_find_all_is_abstract(self):
        """find_all은 추상 메서드여야 한다"""
        assert getattr(BaseRepository.find_all, "__isabstractmethod__", False)

    def test_update_is_abstract(self):
        """update는 추상 메서드여야 한다"""
        assert getattr(BaseRepository.update, "__isabstractmethod__", False)

    def test_delete_is_abstract(self):
        """delete는 추상 메서드여야 한다"""
        assert getattr(BaseRepository.delete, "__isabstractmethod__", False)

    def test_concrete_implementation_must_implement_all_methods(self):
        """모든 추상 메서드를 구현하지 않으면 인스턴스화 불가"""
        class IncompleteRepo(BaseRepository):
            def save(self, entity):
                return entity

        with pytest.raises(TypeError):
            IncompleteRepo()

    def test_complete_implementation_can_be_instantiated(self):
        """모든 추상 메서드를 구현하면 인스턴스화 가능"""
        class CompleteRepo(BaseRepository):
            def save(self, entity):
                return entity

            def find_by_id(self, id: str):
                return None

            def find_all(self):
                return []

            def update(self, entity):
                return entity

            def delete(self, id: str):
                return True

        repo = CompleteRepo()
        assert repo is not None
