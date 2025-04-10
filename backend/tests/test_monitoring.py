import pytest
from datetime import datetime, timedelta
from ..services.monitoring_service import MonitoringService
from ..models.monitoring import Metric, Alert, AlertHistory
from ..schemas.monitoring import (
    MetricCreate,
    AlertCreate,
    AlertUpdate,
    MetricCondition,
    AlertSeverity,
    AlertStatus
)

@pytest.fixture
def db_session(test_db):
    return test_db

@pytest.fixture
def monitoring_service(db_session):
    return MonitoringService(db_session)

async def test_record_metric(monitoring_service):
    metric = MetricCreate(
        name="test_metric",
        value=42.0,
        labels={"source": "test"},
        metadata={"test": True}
    )
    
    recorded_metric = await monitoring_service.record_metric(metric)
    
    assert recorded_metric.id is not None
    assert recorded_metric.name == "test_metric"
    assert recorded_metric.value == 42.0
    assert recorded_metric.labels == {"source": "test"}

async def test_create_alert(monitoring_service):
    alert = AlertCreate(
        metric_name="test_metric",
        condition=MetricCondition.GREATER_THAN,
        threshold=40.0,
        severity=AlertSeverity.WARNING,
        metadata={"test": True}
    )
    
    created_alert = await monitoring_service.create_alert(alert)
    
    assert created_alert.id is not None
    assert created_alert.metric_name == "test_metric"
    assert created_alert.condition == "gt"
    assert created_alert.threshold == 40.0
    assert created_alert.severity == "warning"

async def test_alert_triggering(monitoring_service):
    # Создаем алерт
    alert = AlertCreate(
        metric_name="test_metric",
        condition=MetricCondition.GREATER_THAN,
        threshold=40.0,
        severity=AlertSeverity.WARNING
    )
    created_alert = await monitoring_service.create_alert(alert)
    
    # Записываем метрику, которая должна вызвать алерт
    metric = MetricCreate(
        name="test_metric",
        value=42.0
    )
    await monitoring_service.record_metric(metric)
    
    # Проверяем историю алертов
    history = await monitoring_service.get_alert_history(created_alert.id)
    assert len(history) == 1
    assert history[0].metric_value == 42.0

async def test_update_alert(monitoring_service):
    # Создаем алерт
    alert = AlertCreate(
        metric_name="test_metric",
        condition=MetricCondition.GREATER_THAN,
        threshold=40.0,
        severity=AlertSeverity.WARNING
    )
    created_alert = await monitoring_service.create_alert(alert)
    
    # Обновляем статус алерта
    update = AlertUpdate(status=AlertStatus.RESOLVED)
    updated_alert = await monitoring_service.update_alert(created_alert.id, update)
    
    assert updated_alert.status == "resolved"
    assert updated_alert.resolved_at is not None

async def test_get_metrics(monitoring_service):
    # Записываем несколько метрик
    for i in range(3):
        metric = MetricCreate(
            name=f"test_metric_{i}",
            value=float(i)
        )
        await monitoring_service.record_metric(metric)
    
    # Получаем все метрики
    metrics = await monitoring_service.get_metrics()
    assert len(metrics) >= 3
    
    # Получаем метрики по имени
    metrics = await monitoring_service.get_metrics(name="test_metric_1")
    assert len(metrics) == 1
    assert metrics[0].value == 1.0

async def test_get_alerts(monitoring_service):
    # Создаем несколько алертов
    for severity in ["info", "warning", "critical"]:
        alert = AlertCreate(
            metric_name="test_metric",
            condition=MetricCondition.GREATER_THAN,
            threshold=40.0,
            severity=severity
        )
        await monitoring_service.create_alert(alert)
    
    # Получаем все алерты
    alerts = await monitoring_service.get_alerts()
    assert len(alerts) >= 3
    
    # Получаем алерты по серьезности
    alerts = await monitoring_service.get_alerts(severity="critical")
    assert len(alerts) == 1
    assert alerts[0].severity == "critical"

async def test_get_monitoring_summary(monitoring_service):
    # Создаем тестовые данные
    for i in range(3):
        metric = MetricCreate(
            name=f"test_metric_{i}",
            value=float(i)
        )
        await monitoring_service.record_metric(metric)
        
        alert = AlertCreate(
            metric_name=f"test_metric_{i}",
            condition=MetricCondition.GREATER_THAN,
            threshold=0.0,
            severity=["info", "warning", "critical"][i]
        )
        await monitoring_service.create_alert(alert)
    
    summary = await monitoring_service.get_monitoring_summary()
    
    assert summary.total_metrics >= 3
    assert summary.active_alerts >= 3
    assert summary.critical_alerts >= 1
    assert summary.warning_alerts >= 1
    assert summary.info_alerts >= 1
    assert len(summary.metrics_by_name) >= 3
    assert len(summary.alerts_by_severity) >= 3 