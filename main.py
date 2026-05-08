"""DataPersistence PoC - JSON 기반 CRUD 흐름 시연"""
from datetime import datetime
from pathlib import Path

from app.model.enums import OrderStatus
from app.model.order import Order
from app.model.sample import Sample
from app.repository.json.json_order_repo import JsonOrderRepository
from app.repository.json.json_sample_repo import JsonSampleRepository

DATA_DIR = Path(__file__).parent / "data"


def demo_sample_crud(sample_repo: JsonSampleRepository) -> None:
    """Sample CRUD 시연"""
    print("\n=== Sample CRUD 시연 ===")

    # Create
    sample = Sample(
        id="S-001",
        name="실리콘 웨이퍼-8인치",
        avg_production_time=0.5,
        yield_rate=0.92,
        stock=480,
    )
    saved = sample_repo.save(sample)
    print(f"[Create] 저장: {saved.id} - {saved.name} (재고: {saved.stock})")

    sample2 = Sample(
        id="S-002",
        name="갈륨 비소 웨이퍼",
        avg_production_time=1.2,
        yield_rate=0.85,
        stock=200,
    )
    sample_repo.save(sample2)
    print(f"[Create] 저장: {sample2.id} - {sample2.name}")

    # Read
    found = sample_repo.find_by_id("S-001")
    print(f"[Read] ID 조회: {found.id} - {found.name}")

    all_samples = sample_repo.find_all()
    print(f"[Read] 전체 조회: {len(all_samples)}개")

    search_results = sample_repo.find_by_name("웨이퍼")
    print(f"[Read] '웨이퍼' 검색: {len(search_results)}개")

    # Update (stock)
    updated = sample_repo.update_stock("S-001", -50)
    print(f"[Update] 재고 변경: {updated.id} 재고 {480} → {updated.stock}")

    # Delete
    result = sample_repo.delete("S-002")
    print(f"[Delete] S-002 삭제: {'성공' if result else '실패'}")
    print(f"[Delete] 삭제 후 전체: {len(sample_repo.find_all())}개")


def demo_order_crud(order_repo: JsonOrderRepository) -> None:
    """Order CRUD 시연"""
    print("\n=== Order CRUD 시연 ===")

    # Create
    order = Order(
        order_no="ORD-20260508-0001",
        sample_id="S-001",
        customer_name="삼성전자 파운드리",
        quantity=200,
        status=OrderStatus.RESERVED,
        created_at=datetime(2026, 5, 8, 9, 32, 15),
    )
    saved = order_repo.save(order)
    print(f"[Create] 주문 저장: {saved.order_no} (상태: {saved.status.value})")

    order2 = Order(
        order_no="ORD-20260508-0002",
        sample_id="S-001",
        customer_name="SK하이닉스",
        quantity=150,
        status=OrderStatus.PRODUCING,
        created_at=datetime(2026, 5, 8, 10, 0, 0),
    )
    order_repo.save(order2)

    # Read
    found = order_repo.find_by_id("ORD-20260508-0001")
    print(f"[Read] 주문 조회: {found.order_no} - {found.customer_name}")

    reserved_orders = order_repo.find_by_status(OrderStatus.RESERVED)
    print(f"[Read] RESERVED 주문: {len(reserved_orders)}개")

    sample_orders = order_repo.find_by_sample("S-001")
    print(f"[Read] S-001 관련 주문: {len(sample_orders)}개")

    # Update (status)
    updated = order_repo.update_status("ORD-20260508-0001", OrderStatus.PRODUCING)
    print(f"[Update] 상태 변경: {updated.order_no} → {updated.status.value}")

    # Delete
    result = order_repo.delete("ORD-20260508-0002")
    print(f"[Delete] ORD-20260508-0002 삭제: {'성공' if result else '실패'}")
    print(f"[Delete] 삭제 후 전체: {len(order_repo.find_all())}개")


def demo_persistence(data_dir: Path) -> None:
    """영속성 검증: 인스턴스 재생성 후 데이터 유지"""
    print("\n=== 영속성 검증 ===")

    sample_path = data_dir / "samples.json"
    order_path = data_dir / "orders.json"

    # 데이터 저장
    repo1 = JsonSampleRepository(sample_path)
    repo1.save(Sample(
        id="S-PERSIST",
        name="영속성 테스트 시료",
        avg_production_time=1.0,
        yield_rate=0.9,
        stock=100,
    ))
    print("[Persistence] 첫 번째 인스턴스로 저장 완료")

    # 새 인스턴스로 조회
    repo2 = JsonSampleRepository(sample_path)
    result = repo2.find_by_id("S-PERSIST")
    if result:
        print(f"[Persistence] 새 인스턴스 조회 성공: {result.id} - {result.name}")
    else:
        print("[Persistence] 조회 실패 - 영속성 오류!")


def main() -> None:
    """메인 실행 함수"""
    print("DataPersistence PoC - CRUD 흐름 시연")
    print("=" * 50)

    DATA_DIR.mkdir(exist_ok=True)

    sample_path = DATA_DIR / "samples.json"
    order_path = DATA_DIR / "orders.json"

    # 기존 데이터 초기화 (새 시연을 위해)
    if sample_path.exists():
        sample_path.unlink()
    if order_path.exists():
        order_path.unlink()

    sample_repo = JsonSampleRepository(sample_path)
    order_repo = JsonOrderRepository(order_path)

    demo_sample_crud(sample_repo)
    demo_order_crud(order_repo)
    demo_persistence(DATA_DIR)

    print("\n=== 완료 ===")
    print(f"데이터 저장 경로: {DATA_DIR}")


if __name__ == "__main__":
    main()
