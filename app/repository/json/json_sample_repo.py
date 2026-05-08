"""JSON 파일 기반 SampleRepository 구현체"""
import dataclasses
import json
import os
from pathlib import Path
from typing import Union

from app.model.sample import Sample
from app.repository.sample_repository import SampleRepository


class JsonSampleRepository(SampleRepository):
    """JSON 파일 기반 시료 Repository 구현체

    저장 규칙:
    - 파일이 없으면 [] 로 자동 생성
    - Atomic Write: .tmp 임시 파일 → os.replace() 원자적 교체
    - dataclasses.asdict() 직렬화
    """

    def __init__(self, file_path: Union[str, Path]) -> None:
        self._file_path = Path(file_path)
        self._ensure_file()

    # ------------------------------------------------------------------
    # 내부 헬퍼
    # ------------------------------------------------------------------

    def _ensure_file(self) -> None:
        """파일이 없으면 빈 JSON 배열로 자동 생성한다."""
        if not self._file_path.exists():
            self._write_atomic([])

    def _load(self) -> list[dict]:
        """JSON 파일을 읽어 dict 리스트로 반환한다."""
        with open(self._file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_atomic(self, records: list[dict]) -> None:
        """임시 파일에 쓴 후 os.replace로 원자적으로 교체한다."""
        tmp_path = self._file_path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self._file_path)

    def _to_dict(self, sample: Sample) -> dict:
        """Sample을 JSON 직렬화 가능한 dict로 변환한다."""
        return dataclasses.asdict(sample)

    def _from_dict(self, data: dict) -> Sample:
        """dict에서 Sample 인스턴스를 복원한다."""
        return Sample(
            id=data["id"],
            name=data["name"],
            avg_production_time=float(data["avg_production_time"]),
            yield_rate=float(data["yield_rate"]),
            stock=int(data["stock"]),
        )

    # ------------------------------------------------------------------
    # BaseRepository CRUD 구현
    # ------------------------------------------------------------------

    def save(self, entity: Sample) -> Sample:
        """시료를 JSON 파일에 저장한다."""
        records = self._load()
        records.append(self._to_dict(entity))
        self._write_atomic(records)
        return entity

    def find_by_id(self, id: str) -> Sample | None:
        """ID로 시료를 조회한다."""
        for record in self._load():
            if record["id"] == id:
                return self._from_dict(record)
        return None

    def find_all(self) -> list[Sample]:
        """모든 시료를 조회한다."""
        return [self._from_dict(r) for r in self._load()]

    def update(self, entity: Sample) -> Sample:
        """시료 정보를 업데이트한다."""
        records = self._load()
        for i, record in enumerate(records):
            if record["id"] == entity.id:
                records[i] = self._to_dict(entity)
                self._write_atomic(records)
                return entity
        raise ValueError(f"Sample not found: {entity.id}")

    def delete(self, id: str) -> bool:
        """ID로 시료를 삭제한다."""
        records = self._load()
        new_records = [r for r in records if r["id"] != id]
        if len(new_records) == len(records):
            return False
        self._write_atomic(new_records)
        return True

    # ------------------------------------------------------------------
    # SampleRepository 특화 메서드 구현
    # ------------------------------------------------------------------

    def find_by_name(self, keyword: str) -> list[Sample]:
        """키워드로 시료를 검색한다 (부분 일치)."""
        return [
            self._from_dict(r)
            for r in self._load()
            if keyword in r["name"]
        ]

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
        records = self._load()
        for i, record in enumerate(records):
            if record["id"] == sample_id:
                record["stock"] = record["stock"] + delta
                records[i] = record
                self._write_atomic(records)
                return self._from_dict(record)
        raise ValueError(f"Sample not found: {sample_id}")
