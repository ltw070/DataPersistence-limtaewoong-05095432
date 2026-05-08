"""Phase 3: JsonSampleRepository PRD 검증 기준 5개 테스트 (tmp_path 사용)"""
import json
import pytest
from pathlib import Path
from app.model.sample import Sample
from app.repository.json.json_sample_repo import JsonSampleRepository

# 공통 픽스처는 conftest.py에서 제공:
# sample_repo, sample_file_path, sample_a, sample_b


class TestSampleSave:
    """test_sample_save: save 후 파일에 실제로 기록되는지 확인"""

    def test_sample_save_creates_file(self, sample_file_path, sample_a):
        """save 후 samples.json 파일이 생성되어야 한다"""
        repo = JsonSampleRepository(sample_file_path)
        repo.save(sample_a)
        assert sample_file_path.exists()

    def test_sample_save_writes_to_file(self, sample_file_path, sample_a):
        """save 후 파일에 시료 데이터가 기록되어야 한다"""
        repo = JsonSampleRepository(sample_file_path)
        repo.save(sample_a)

        with open(sample_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["id"] == "S-001"
        assert data[0]["name"] == "실리콘 웨이퍼-8인치"
        assert data[0]["stock"] == 480

    def test_sample_save_returns_entity(self, sample_repo, sample_a):
        """save는 저장된 엔티티를 반환해야 한다"""
        result = sample_repo.save(sample_a)
        assert result == sample_a

    def test_sample_save_multiple(self, sample_repo, sample_a, sample_b):
        """여러 시료를 저장할 수 있어야 한다"""
        sample_repo.save(sample_a)
        sample_repo.save(sample_b)

        all_samples = sample_repo.find_all()
        assert len(all_samples) == 2

    def test_sample_save_file_auto_created_if_not_exists(self, tmp_path):
        """파일이 없어도 자동 생성되어야 한다"""
        file_path = tmp_path / "new_samples.json"
        assert not file_path.exists()

        repo = JsonSampleRepository(file_path)
        sample = Sample(id="S-999", name="테스트", avg_production_time=1.0, yield_rate=0.9, stock=10)
        repo.save(sample)

        assert file_path.exists()


class TestSampleFindById:
    """test_sample_find_by_id: 저장된 Sample을 id로 정확히 조회"""

    def test_find_existing_sample(self, sample_repo, sample_a):
        """저장된 시료를 id로 조회해야 한다"""
        sample_repo.save(sample_a)
        result = sample_repo.find_by_id("S-001")
        assert result is not None
        assert result.id == "S-001"
        assert result.name == "실리콘 웨이퍼-8인치"

    def test_find_nonexistent_sample_returns_none(self, sample_repo):
        """존재하지 않는 id로 조회하면 None을 반환해야 한다"""
        result = sample_repo.find_by_id("S-999")
        assert result is None

    def test_find_by_id_returns_correct_sample(self, sample_repo, sample_a, sample_b):
        """여러 시료 중 정확한 시료를 반환해야 한다"""
        sample_repo.save(sample_a)
        sample_repo.save(sample_b)

        result = sample_repo.find_by_id("S-002")
        assert result is not None
        assert result.id == "S-002"
        assert result.name == "갈륨 비소 웨이퍼"

    def test_find_by_id_returns_sample_instance(self, sample_repo, sample_a):
        """find_by_id는 Sample 인스턴스를 반환해야 한다"""
        sample_repo.save(sample_a)
        result = sample_repo.find_by_id("S-001")
        assert isinstance(result, Sample)

    def test_find_all_returns_all_samples(self, sample_repo, sample_a, sample_b):
        """find_all은 모든 시료를 반환해야 한다"""
        sample_repo.save(sample_a)
        sample_repo.save(sample_b)

        results = sample_repo.find_all()
        assert len(results) == 2
        ids = [s.id for s in results]
        assert "S-001" in ids
        assert "S-002" in ids


class TestSampleUpdateStock:
    """test_sample_update_stock: delta 적용 후 stock 값 변경 확인"""

    def test_update_stock_increase(self, sample_repo, sample_a):
        """delta 양수: 재고가 증가해야 한다"""
        sample_repo.save(sample_a)
        result = sample_repo.update_stock("S-001", 100)

        assert result.stock == 580  # 480 + 100

    def test_update_stock_decrease(self, sample_repo, sample_a):
        """delta 음수: 재고가 감소해야 한다"""
        sample_repo.save(sample_a)
        result = sample_repo.update_stock("S-001", -50)

        assert result.stock == 430  # 480 - 50

    def test_update_stock_persisted_to_file(self, sample_file_path, sample_a):
        """update_stock 후 변경사항이 파일에 반영되어야 한다"""
        repo = JsonSampleRepository(sample_file_path)
        repo.save(sample_a)
        repo.update_stock("S-001", 20)

        with open(sample_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data[0]["stock"] == 500  # 480 + 20

    def test_update_stock_nonexistent_raises_error(self, sample_repo):
        """존재하지 않는 시료의 재고 변경은 ValueError를 발생시켜야 한다"""
        with pytest.raises(ValueError):
            sample_repo.update_stock("S-999", 10)

    def test_find_by_name_keyword_match(self, sample_repo, sample_a, sample_b):
        """키워드로 시료를 검색할 수 있어야 한다"""
        sample_repo.save(sample_a)
        sample_repo.save(sample_b)

        results = sample_repo.find_by_name("웨이퍼")
        assert len(results) == 2

    def test_find_by_name_partial_match(self, sample_repo, sample_a, sample_b):
        """부분 일치 검색이 동작해야 한다"""
        sample_repo.save(sample_a)
        sample_repo.save(sample_b)

        results = sample_repo.find_by_name("실리콘")
        assert len(results) == 1
        assert results[0].id == "S-001"


class TestSampleDelete:
    """test_sample_delete: 삭제 후 find_by_id → None 반환 확인"""

    def test_delete_existing_sample(self, sample_repo, sample_a):
        """존재하는 시료를 삭제할 수 있어야 한다"""
        sample_repo.save(sample_a)
        result = sample_repo.delete("S-001")
        assert result is True

    def test_delete_then_find_returns_none(self, sample_repo, sample_a):
        """삭제 후 find_by_id는 None을 반환해야 한다"""
        sample_repo.save(sample_a)
        sample_repo.delete("S-001")

        result = sample_repo.find_by_id("S-001")
        assert result is None

    def test_delete_removes_from_file(self, sample_file_path, sample_a):
        """삭제 후 파일에서도 제거되어야 한다"""
        repo = JsonSampleRepository(sample_file_path)
        repo.save(sample_a)
        repo.delete("S-001")

        with open(sample_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 0

    def test_delete_nonexistent_returns_false(self, sample_repo):
        """존재하지 않는 시료 삭제는 False를 반환해야 한다"""
        result = sample_repo.delete("S-999")
        assert result is False

    def test_delete_only_removes_target(self, sample_repo, sample_a, sample_b):
        """삭제 시 대상 시료만 제거해야 한다"""
        sample_repo.save(sample_a)
        sample_repo.save(sample_b)
        sample_repo.delete("S-001")

        all_samples = sample_repo.find_all()
        assert len(all_samples) == 1
        assert all_samples[0].id == "S-002"


class TestSamplePersistence:
    """test_sample_persistence: 인스턴스 새로 생성 후에도 데이터 유지 확인"""

    def test_data_persists_after_new_instance(self, sample_file_path, sample_a):
        """새 인스턴스를 생성해도 이전에 저장한 데이터가 유지되어야 한다"""
        repo1 = JsonSampleRepository(sample_file_path)
        repo1.save(sample_a)

        # 새 인스턴스로 조회 (영속성 핵심 테스트)
        repo2 = JsonSampleRepository(sample_file_path)
        result = repo2.find_by_id("S-001")

        assert result is not None
        assert result.id == "S-001"
        assert result.name == "실리콘 웨이퍼-8인치"
        assert result.stock == 480

    def test_all_fields_persist(self, sample_file_path, sample_a):
        """모든 필드가 영속성을 유지해야 한다"""
        repo1 = JsonSampleRepository(sample_file_path)
        repo1.save(sample_a)

        repo2 = JsonSampleRepository(sample_file_path)
        result = repo2.find_by_id("S-001")

        assert result.avg_production_time == 0.5
        assert result.yield_rate == 0.92

    def test_multiple_saves_persist(self, sample_file_path, sample_a, sample_b):
        """여러 시료가 영속성을 유지해야 한다"""
        repo1 = JsonSampleRepository(sample_file_path)
        repo1.save(sample_a)
        repo1.save(sample_b)

        repo2 = JsonSampleRepository(sample_file_path)
        all_samples = repo2.find_all()

        assert len(all_samples) == 2

    def test_update_persists(self, sample_file_path, sample_a):
        """update 후 새 인스턴스에서도 변경사항이 유지되어야 한다"""
        repo1 = JsonSampleRepository(sample_file_path)
        repo1.save(sample_a)
        sample_a.name = "수정된 시료명"
        repo1.update(sample_a)

        repo2 = JsonSampleRepository(sample_file_path)
        result = repo2.find_by_id("S-001")

        assert result.name == "수정된 시료명"

    def test_delete_persists(self, sample_file_path, sample_a):
        """삭제 후 새 인스턴스에서도 삭제 상태가 유지되어야 한다"""
        repo1 = JsonSampleRepository(sample_file_path)
        repo1.save(sample_a)
        repo1.delete("S-001")

        repo2 = JsonSampleRepository(sample_file_path)
        result = repo2.find_by_id("S-001")

        assert result is None
