# PRD: DataPersistence (데이터 영속성 처리)

> **PoC 목표**: 애플리케이션 재시작 후에도 데이터를 유지할 수 있는 영속성 레이어를 구현한다.  
> **최종 목적지**: `mission2/SampleOrderSystem` 의 Repository 레이어로 그대로 편입된다.

---

## 1. 개요

`PoC1(ConsoleMVC)` 의 도메인 모델(Sample, Order)을 저장·불러오는 Repository 레이어를 설계한다.  
추상 인터페이스를 먼저 정의하고, JSON 파일 기반 구현체를 제공한다.  
Controller는 Repository 인터페이스에만 의존하므로, 구현체를 교체해도 상위 레이어는 영향을 받지 않는다.

---

## 2. 패키지 구조

```
02_DataPersistence/
├── app/
│   ├── model/
│   │   ├── sample.py          # PoC1과 동일한 도메인 객체
│   │   ├── order.py
│   │   ├── production.py
│   │   └── enums.py
│   └── repository/
│       ├── base_repository.py    # 추상 Generic Repository
│       ├── sample_repository.py  # SampleRepository 인터페이스
│       ├── order_repository.py   # OrderRepository 인터페이스
│       └── json/
│           ├── json_sample_repo.py
│           └── json_order_repo.py
├── tests/
│   ├── test_model/
│   └── test_repository/
│       ├── test_sample_repository.py
│       └── test_order_repository.py
├── data/                          # 런타임 저장 경로 (.gitignore)
├── main.py                        # CRUD 동작 시연
└── requirements.txt
```

---

## 3. 도메인 모델

PoC1과 동일한 모델을 사용한다. (공통 인터페이스 유지)

```python
# model/enums.py
class OrderStatus(Enum):
    RESERVED  = "RESERVED"
    REJECTED  = "REJECTED"
    PRODUCING = "PRODUCING"
    CONFIRMED = "CONFIRMED"
    RELEASE   = "RELEASE"

# model/sample.py
@dataclass
class Sample:
    id: str                      # "S-001" 형식
    name: str
    avg_production_time: float   # min/ea, 양수
    yield_rate: float            # 0 < yield_rate <= 1
    stock: int                   # 0 이상

# model/order.py
@dataclass
class Order:
    order_no: str                # "ORD-YYYYMMDD-XXXX" 형식
    sample_id: str
    customer_name: str
    quantity: int                # 양수
    status: OrderStatus
    created_at: datetime
```

---

## 4. Repository 인터페이스

### 4.1 BaseRepository (Generic)

```python
T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def save(self, entity: T) -> T: ...

    @abstractmethod
    def find_by_id(self, id: str) -> T | None: ...

    @abstractmethod
    def find_all(self) -> list[T]: ...

    @abstractmethod
    def update(self, entity: T) -> T: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...
```

### 4.2 SampleRepository

```python
class SampleRepository(BaseRepository[Sample]):
    def find_by_name(self, keyword: str) -> list[Sample]: ...
    def update_stock(self, sample_id: str, delta: int) -> Sample: ...
    # delta 양수 = 재고 증가, 음수 = 재고 감소
```

### 4.3 OrderRepository

```python
class OrderRepository(BaseRepository[Order]):
    def find_by_status(self, status: OrderStatus) -> list[Order]: ...
    def find_by_sample(self, sample_id: str) -> list[Order]: ...
    def update_status(self, order_no: str, status: OrderStatus) -> Order: ...
```

---

## 5. JSON 구현체 명세

### 저장 경로

```
data/
├── samples.json
└── orders.json
```

### samples.json 스키마

```json
[
  {
    "id": "S-001",
    "name": "실리콘 웨이퍼-8인치",
    "avg_production_time": 0.5,
    "yield_rate": 0.92,
    "stock": 480
  }
]
```

### orders.json 스키마

```json
[
  {
    "order_no": "ORD-20260508-0001",
    "sample_id": "S-001",
    "customer_name": "삼성전자 파운드리",
    "quantity": 200,
    "status": "RESERVED",
    "created_at": "2026-05-08T09:32:15"
  }
]
```

### 구현 규칙

- 파일이 없으면 자동 생성한다
- 저장 시 전체 리스트를 덮어쓴다 (atomic write: 임시 파일 → rename)
- `dataclass` ↔ `dict` 직렬화는 `dataclasses.asdict` / 커스텀 decoder로 처리한다
- `OrderStatus` Enum은 문자열 값으로 직렬화한다
- `datetime`은 ISO 8601 문자열로 직렬화한다

---

## 6. 검증 기준 (TDD)

모든 테스트는 `pytest`의 `tmp_path` fixture로 임시 경로를 사용한다.

| 테스트 | 검증 내용 |
|--------|----------|
| `test_sample_save` | save 후 파일에 실제로 기록되는지 확인 |
| `test_sample_find_by_id` | 저장된 Sample을 id로 정확히 조회 |
| `test_sample_update_stock` | delta 적용 후 stock 값 변경 확인 |
| `test_sample_delete` | 삭제 후 find_by_id → None 반환 확인 |
| `test_sample_persistence` | 인스턴스 새로 생성 후에도 데이터 유지 확인 |
| `test_order_save` | RESERVED 상태로 저장 확인 |
| `test_order_find_by_status` | 상태별 필터링 정확성 확인 |
| `test_order_update_status` | 상태 전이 후 파일에 반영 확인 |
| `test_order_persistence` | 인스턴스 재생성 후 주문 데이터 유지 확인 |

커버리지 목표: **80% 이상**
