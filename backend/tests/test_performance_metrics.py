import pytest
from datetime import datetime
from ..services.performance_metrics import PerformanceMetricsService
from ..models.monitoring import Metric
from ..schemas.monitoring import MetricCreate

@pytest.fixture
def db_session(test_db):
    return test_db

@pytest.fixture
def performance_service(db_session):
    return PerformanceMetricsService(db_session)

async def test_collect_system_metrics(performance_service):
    await performance_service.collect_system_metrics()
    
    # Проверяем, что метрики CPU были записаны
    cpu_metrics = performance_service.db.query(Metric).filter(
        Metric.name.like("system.cpu.%")
    ).all()
    assert len(cpu_metrics) > 0
    
    # Проверяем, что метрики памяти были записаны
    memory_metrics = performance_service.db.query(Metric).filter(
        Metric.name.like("system.memory.%")
    ).all()
    assert len(memory_metrics) > 0
    
    # Проверяем, что метрики диска были записаны
    disk_metrics = performance_service.db.query(Metric).filter(
        Metric.name.like("system.disk.%")
    ).all()
    assert len(disk_metrics) > 0

async def test_collect_application_metrics(performance_service):
    await performance_service.collect_application_metrics()
    
    # Проверяем, что метрики GC были записаны
    gc_metrics = performance_service.db.query(Metric).filter(
        Metric.name.like("app.gc.%")
    ).all()
    assert len(gc_metrics) > 0
    
    # Проверяем, что метрики памяти приложения были записаны
    memory_metrics = performance_service.db.query(Metric).filter(
        Metric.name.like("app.memory.%")
    ).all()
    assert len(memory_metrics) > 0

async def test_collect_database_metrics(performance_service):
    await performance_service.collect_database_metrics()
    
    # Проверяем, что метрики базы данных были записаны
    db_metrics = performance_service.db.query(Metric).filter(
        Metric.name.like("db.%")
    ).all()
    assert len(db_metrics) > 0

async def test_collect_api_metrics(performance_service):
    await performance_service.collect_api_metrics(
        endpoint="/test",
        method="GET",
        duration=0.1,
        status_code=200
    )
    
    # Проверяем, что метрики API были записаны
    api_metrics = performance_service.db.query(Metric).filter(
        Metric.name.like("api.%")
    ).all()
    assert len(api_metrics) > 0
    
    # Проверяем метки
    for metric in api_metrics:
        assert "endpoint" in metric.labels
        assert "method" in metric.labels
        assert "status_code" in metric.labels

async def test_collect_cache_metrics(performance_service):
    await performance_service.collect_cache_metrics(
        operation="get",
        duration=0.05,
        success=True
    )
    
    # Проверяем, что метрики кэша были записаны
    cache_metrics = performance_service.db.query(Metric).filter(
        Metric.name.like("cache.%")
    ).all()
    assert len(cache_metrics) > 0
    
    # Проверяем метки
    for metric in cache_metrics:
        assert "operation" in metric.labels
        assert "success" in metric.labels

async def test_collect_all_metrics(performance_service):
    await performance_service.collect_all_metrics()
    
    # Проверяем, что метрики сбора были записаны
    collection_metrics = performance_service.db.query(Metric).filter(
        Metric.name == "metrics.collection.duration"
    ).all()
    assert len(collection_metrics) == 1
    
    # Проверяем, что время сбора записано
    assert collection_metrics[0].value > 0

async def test_error_handling(performance_service):
    # Имитируем ошибку при сборе метрик
    original_collect_system_metrics = performance_service.collect_system_metrics
    performance_service.collect_system_metrics = lambda: 1/0
    
    await performance_service.collect_all_metrics()
    
    # Проверяем, что ошибка была записана
    error_metrics = performance_service.db.query(Metric).filter(
        Metric.name == "metrics.collection.error"
    ).all()
    assert len(error_metrics) == 1
    
    # Восстанавливаем оригинальный метод
    performance_service.collect_system_metrics = original_collect_system_metrics 