# PLAN: DataPersistence (데이터 영속성 처리)

## 목표

애플리케이션 재시작 후에도 데이터를 유지할 수 있는 Repository 레이어를 설계하고, JSON 파일 기반 구현체를 TDD로 검증하여 `mission2/SampleOrderSystem`의 Repository 레이어로 편입한다.

---

## 구현 순서 (TDD: Red → Green → Refactor)

### Phase 1 – 도메인 모델

PoC1(ConsoleMVC)과 동일한 인터페이스를 유지한다.

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Red | `tests/test_model/test_sample.py` | Sample dataclass 필드 타입·기본값 검증 테스트 작성 |
| Red | `tests/test_model/test_order.py` | Order dataclass 필드 타입·OrderStatus Enum 검증 테스트 작성 |
| Green | `app/model/enums.py` | `OrderStatus(Enum)` 정의: RESERVED, REJECTED, PRODUCING, CONFIRMED, RELEASE |
| Green | `app/model/sample.py` | `@dataclass Sample` 정의: id, name, avg_production_time, yield_rate, stock |
| Green | `app/model/order.py` | `@dataclass Order` 정의: order_no, sample_id, customer_name, quantity, status, created_at |
| Green | `app/model/production.py` | 생산 관련 보조 모델 정의 |
| Refactor | `app/model/` | `__init__.py` 정리, 공개 API export 확인 |

### Phase 2 – Repository 인터페이스

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Red | `tests/test_repository/test_base_repository.py` | 추상 메서드 목록(save, find_by_id, find_all, update, delete) 존재 확인 테스트 |
| Red | `tests/test_repository/test_interface_sample.py` | SampleRepository 추가 메서드(find_by_name, update_stock) 시그니처 확인 테스트 |
| Red | `tests/test_repository/test_interface_order.py` | OrderRepository 추가 메서드(find_by_status, find_by_sample, update_status) 시그니처 확인 테스트 |
| Green | `app/repository/base_repository.py` | `BaseRepository(ABC, Generic[T])`: save, find_by_id, find_all, update, delete 추상 메서드 |
| Green | `app/repository/sample_repository.py` | `SampleRepository(BaseRepository[Sample])`: find_by_name, update_stock 추상 메서드 |
| Green | `app/repository/order_repository.py` | `OrderRepository(BaseRepository[Order])`: find_by_status, find_by_sample, update_status 추상 메서드 |
| Refactor | `app/repository/` | `__init__.py` 정리, 타입 힌트 일관성 점검 |

### Phase 3 – JSON 구현체

PRD Section 6 검증 기준 9개 테스트를 Red 단계에서 모두 작성한다.

#### Red 단계 – 9개 테스트

| 단계 | 파일 | 테스트 ID | 검증 내용 |
|------|------|-----------|----------|
| Red | `tests/test_repository/test_sample_repository.py` | `test_sample_save` | save 후 samples.json 파일에 실제로 기록되는지 확인 |
| Red | `tests/test_repository/test_sample_repository.py` | `test_sample_find_by_id` | 저장된 Sample을 id로 정확히 조회 |
| Red | `tests/test_repository/test_sample_repository.py` | `test_sample_update_stock` | delta 적용 후 stock 값 변경 확인 |
| Red | `tests/test_repository/test_sample_repository.py` | `test_sample_delete` | 삭제 후 find_by_id → None 반환 확인 |
| Red | `tests/test_repository/test_sample_repository.py` | `test_sample_persistence` | 인스턴스 새로 생성 후에도 데이터 유지 확인 |
| Red | `tests/test_repository/test_order_repository.py` | `test_order_save` | RESERVED 상태로 저장 확인 |
| Red | `tests/test_repository/test_order_repository.py` | `test_order_find_by_status` | 상태별 필터링 정확성 확인 |
| Red | `tests/test_repository/test_order_repository.py` | `test_order_update_status` | 상태 전이 후 파일에 반영 확인 |
| Red | `tests/test_repository/test_order_repository.py` | `test_order_persistence` | 인스턴스 재생성 후 주문 데이터 유지 확인 |

모든 테스트는 `pytest`의 `tmp_path` fixture를 사용하여 실제 `data/` 디렉토리를 오염시키지 않는다.

#### Green 단계 – JSON 구현체

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Green | `app/repository/json/json_sample_repo.py` | `JsonSampleRepository(SampleRepository)` 구현 |
| Green | `app/repository/json/json_order_repo.py` | `JsonOrderRepository(OrderRepository)` 구현 |

**JSON 구현 규칙 (반드시 준수):**

1. **파일 자동 생성**: 지정 경로에 파일이 없으면 `[]`로 자동 생성
2. **Atomic Write**: 저장 시 `.tmp` 임시 파일에 먼저 쓴 후 `os.replace(tmp, target)` 로 원자적 교체
3. **Enum 직렬화**: `OrderStatus` 값을 문자열로 직렬화 (`"RESERVED"`, `"PRODUCING"` 등)
4. **datetime 직렬화**: ISO 8601 문자열로 직렬화 (`"2026-05-08T09:32:15"`)
5. **직렬화/역직렬화**: `dataclasses.asdict()` → Enum·datetime 문자열 변환 / 커스텀 decoder로 복원

#### Refactor 단계

| 단계 | 대상 | 작업 내용 |
|------|------|----------|
| Refactor | `app/repository/json/` | 직렬화/역직렬화 공통 로직을 내부 헬퍼로 분리 |
| Refactor | `app/repository/json/` | atomic write 로직을 공통 베이스 메서드로 추출 |
| Refactor | `tests/` | 공통 fixture를 `conftest.py`로 분리 |

### Phase 4 – 통합 검증 및 커버리지

| 단계 | 파일 | 작업 내용 |
|------|------|----------|
| Green | `requirements.txt` | pytest, pytest-cov 의존성 추가 |
| Green | `main.py` | JSON 구현체를 사용한 CRUD 전체 흐름 시연 |
| 검증 | — | `pytest tests/ -v --cov=app --cov-report=term-missing` 실행 |

---

## 커밋 전략

| prefix | 시점 |
|--------|------|
| `test:` | Red 단계 완료 시 |
| `feat:` | Green 단계 완료 시 |
| `refactor:` | Refactor 단계 완료 시 |

---

## 완료 기준

- [ ] 모든 테스트 통과 (`pytest`)
- [ ] 커버리지 80% 이상
- [ ] `tmp_path` fixture 사용한 격리된 테스트
- [ ] Atomic write (임시 파일 → `os.replace`) 구현
- [ ] PRD Section 6 검증 기준 9개 테스트 모두 포함
- [ ] `OrderStatus` Enum 문자열 직렬화 확인
- [ ] `datetime` ISO 8601 직렬화/역직렬화 확인
- [ ] `data/` 디렉토리 `.gitignore` 등록
