"""Phase 1 Red: Sample dataclass 필드 타입 및 기본값 테스트"""
import pytest
from app.model.sample import Sample


class TestSampleFields:
    """Sample dataclass 필드 타입 및 생성 테스트"""

    def test_sample_creation_with_all_fields(self):
        """모든 필드를 제공해 Sample 인스턴스 생성"""
        sample = Sample(
            id="S-001",
            name="실리콘 웨이퍼-8인치",
            avg_production_time=0.5,
            yield_rate=0.92,
            stock=480,
        )
        assert sample.id == "S-001"
        assert sample.name == "실리콘 웨이퍼-8인치"
        assert sample.avg_production_time == 0.5
        assert sample.yield_rate == 0.92
        assert sample.stock == 480

    def test_sample_id_type(self):
        """id 필드는 str 타입이어야 한다"""
        sample = Sample(
            id="S-001",
            name="테스트 시료",
            avg_production_time=1.0,
            yield_rate=0.9,
            stock=100,
        )
        assert isinstance(sample.id, str)

    def test_sample_name_type(self):
        """name 필드는 str 타입이어야 한다"""
        sample = Sample(
            id="S-002",
            name="갈륨 비소 웨이퍼",
            avg_production_time=2.0,
            yield_rate=0.85,
            stock=200,
        )
        assert isinstance(sample.name, str)

    def test_sample_avg_production_time_type(self):
        """avg_production_time 필드는 float 타입이어야 한다"""
        sample = Sample(
            id="S-003",
            name="테스트 시료",
            avg_production_time=0.75,
            yield_rate=0.9,
            stock=50,
        )
        assert isinstance(sample.avg_production_time, float)

    def test_sample_yield_rate_type(self):
        """yield_rate 필드는 float 타입이어야 한다"""
        sample = Sample(
            id="S-004",
            name="테스트 시료",
            avg_production_time=1.0,
            yield_rate=0.95,
            stock=100,
        )
        assert isinstance(sample.yield_rate, float)

    def test_sample_stock_type(self):
        """stock 필드는 int 타입이어야 한다"""
        sample = Sample(
            id="S-005",
            name="테스트 시료",
            avg_production_time=1.0,
            yield_rate=0.9,
            stock=300,
        )
        assert isinstance(sample.stock, int)

    def test_sample_equality(self):
        """동일한 필드값을 가진 Sample 인스턴스는 동등해야 한다"""
        s1 = Sample(
            id="S-001",
            name="실리콘 웨이퍼",
            avg_production_time=0.5,
            yield_rate=0.92,
            stock=480,
        )
        s2 = Sample(
            id="S-001",
            name="실리콘 웨이퍼",
            avg_production_time=0.5,
            yield_rate=0.92,
            stock=480,
        )
        assert s1 == s2

    def test_sample_is_dataclass(self):
        """Sample은 dataclass여야 한다"""
        import dataclasses
        assert dataclasses.is_dataclass(Sample)

    def test_sample_stock_zero_allowed(self):
        """stock은 0을 허용해야 한다"""
        sample = Sample(
            id="S-006",
            name="재고 없는 시료",
            avg_production_time=1.0,
            yield_rate=0.8,
            stock=0,
        )
        assert sample.stock == 0
