"""추상 Generic Repository 기반 인터페이스"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """모든 Repository의 기반이 되는 추상 Generic CRUD 인터페이스

    Type Parameters:
        T: 저장할 도메인 엔티티 타입
    """

    @abstractmethod
    def save(self, entity: T) -> T:
        """엔티티를 저장한다.

        Args:
            entity: 저장할 엔티티

        Returns:
            저장된 엔티티
        """
        ...

    @abstractmethod
    def find_by_id(self, id: str) -> T | None:
        """ID로 엔티티를 조회한다.

        Args:
            id: 조회할 엔티티의 ID

        Returns:
            찾은 엔티티, 없으면 None
        """
        ...

    @abstractmethod
    def find_all(self) -> list[T]:
        """모든 엔티티를 조회한다.

        Returns:
            엔티티 목록
        """
        ...

    @abstractmethod
    def update(self, entity: T) -> T:
        """엔티티를 업데이트한다.

        Args:
            entity: 업데이트할 엔티티

        Returns:
            업데이트된 엔티티
        """
        ...

    @abstractmethod
    def delete(self, id: str) -> bool:
        """ID로 엔티티를 삭제한다.

        Args:
            id: 삭제할 엔티티의 ID

        Returns:
            삭제 성공 여부
        """
        ...
