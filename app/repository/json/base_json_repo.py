"""JSON 파일 기반 Repository 공통 기반 클래스"""
import json
import os
from pathlib import Path
from typing import Union


class BaseJsonRepository:
    """JSON 파일 기반 Repository의 공통 기능을 제공하는 믹스인 클래스

    서브클래스가 사용하는 공통 메서드:
    - _ensure_file(): 파일 없으면 [] 로 자동 생성
    - _load(): JSON 파일을 dict 리스트로 로드
    - _write_atomic(): Atomic Write (임시 파일 -> os.replace)
    """

    def __init__(self, file_path: Union[str, Path]) -> None:
        self._file_path = Path(file_path)
        self._ensure_file()

    def _ensure_file(self) -> None:
        """파일이 없으면 빈 JSON 배열로 자동 생성한다."""
        if not self._file_path.exists():
            self._write_atomic([])

    def _load(self) -> list[dict]:
        """JSON 파일을 읽어 dict 리스트로 반환한다."""
        with open(self._file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_atomic(self, records: list[dict]) -> None:
        """임시 파일에 쓴 후 os.replace로 원자적으로 교체한다.

        전원 차단 등의 비정상 종료에도 파일 무결성을 보장한다.
        """
        tmp_path = self._file_path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self._file_path)
