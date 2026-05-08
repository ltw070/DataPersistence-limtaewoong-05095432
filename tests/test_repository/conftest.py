"""테스트 공통 픽스처 정의"""
import pytest
from datetime import datetime
from pathlib import Path

from app.model.sample import Sample
from app.model.order import Order
from app.model.enums import OrderStatus
from app.repository.json.json_sample_repo import JsonSampleRepository
from app.repository.json.json_order_repo import JsonOrderRepository


# ------------------------------------------------------------------
# 파일 경로 픽스처
# ------------------------------------------------------------------

@pytest.fixture
def sample_file_path(tmp_path):
    """임시 samples.json 경로"""
    return tmp_path / "samples.json"


@pytest.fixture
def order_file_path(tmp_path):
    """임시 orders.json 경로"""
    return tmp_path / "orders.json"


# ------------------------------------------------------------------
# Repository 인스턴스 픽스처
# ------------------------------------------------------------------

@pytest.fixture
def sample_repo(sample_file_path):
    """tmp_path 기반 JsonSampleRepository 픽스처"""
    return JsonSampleRepository(sample_file_path)


@pytest.fixture
def order_repo(order_file_path):
    """tmp_path 기반 JsonOrderRepository 픽스처"""
    return JsonOrderRepository(order_file_path)


# ------------------------------------------------------------------
# 도메인 객체 픽스처
# ------------------------------------------------------------------

@pytest.fixture
def sample_a():
    return Sample(
        id="S-001",
        name="실리콘 웨이퍼-8인치",
        avg_production_time=0.5,
        yield_rate=0.92,
        stock=480,
    )


@pytest.fixture
def sample_b():
    return Sample(
        id="S-002",
        name="갈륨 비소 웨이퍼",
        avg_production_time=1.2,
        yield_rate=0.85,
        stock=200,
    )


@pytest.fixture
def order_reserved():
    return Order(
        order_no="ORD-20260508-0001",
        sample_id="S-001",
        customer_name="삼성전자 파운드리",
        quantity=200,
        status=OrderStatus.RESERVED,
        created_at=datetime(2026, 5, 8, 9, 32, 15),
    )


@pytest.fixture
def order_producing():
    return Order(
        order_no="ORD-20260508-0002",
        sample_id="S-001",
        customer_name="SK하이닉스",
        quantity=150,
        status=OrderStatus.PRODUCING,
        created_at=datetime(2026, 5, 8, 10, 0, 0),
    )


@pytest.fixture
def order_confirmed():
    return Order(
        order_no="ORD-20260508-0003",
        sample_id="S-002",
        customer_name="인텔코리아",
        quantity=100,
        status=OrderStatus.CONFIRMED,
        created_at=datetime(2026, 5, 8, 11, 0, 0),
    )
