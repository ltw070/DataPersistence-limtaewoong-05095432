"""SampleRepository 추상 인터페이스"""
from abc import abstractmethod
from app.model.sample import Sample
from .base_repository import BaseRepository


class SampleRepository(BaseRepository[Sample]):
    """시료(Sample) 전용 Repository 인터페이스

    BaseRepository의 CRUD 메서드에 더해 시료 특화 조회/수정 메서드를 정의한다.
    """

    @abstractmethod
    def find_by_name(self, keyword: str) -> list[Sample]:
        """키워드로 시료를 검색한다.

        Args:
            keyword: 시료명 검색 키워드 (부분 일치)

        Returns:
            검색 결과 시료 목록
        """
        ...

    @abstractmethod
    def update_stock(self, sample_id: str, delta: int) -> Sample:
        """시료의 재고를 delta만큼 변경한다.

        Args:
            sample_id: 재고를 변경할 시료의 ID
            delta: 재고 변화량 (양수 = 증가, 음수 = 감소)

        Returns:
            업데이트된 시료

        Raises:
            ValueError: 시료가 존재하지 않는 경우
        """
        ...
