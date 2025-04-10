from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from ..models.monitoring import Metric, Alert, AlertHistory
from ..schemas.monitoring import (
    MetricCreate,
    AlertCreate,
    AlertUpdate,
    AlertHistoryCreate,
    MonitoringSummary
)

class MonitoringService:
    def __init__(self, db: Session):
        self.db = db

    async def record_metric(self, metric: MetricCreate) -> Metric:
        db_metric = Metric(
            name=metric.name,
            value=metric.value,
            labels=metric.labels,
            metadata=metric.metadata
        )
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        
        # Проверяем алерты для метрики
        await self._check_alerts(db_metric)
        
        return db_metric

    async def _check_alerts(self, metric: Metric) -> None:
        alerts = self.db.query(Alert).filter(
            Alert.metric_name == metric.name,
            Alert.status == "active"
        ).all()
        
        for alert in alerts:
            should_trigger = False
            if alert.condition == "gt" and metric.value > alert.threshold:
                should_trigger = True
            elif alert.condition == "lt" and metric.value < alert.threshold:
                should_trigger = True
            elif alert.condition == "eq" and metric.value == alert.threshold:
                should_trigger = True
            elif alert.condition == "neq" and metric.value != alert.threshold:
                should_trigger = True
                
            if should_trigger:
                history = AlertHistory(
                    alert_id=alert.id,
                    metric_value=metric.value,
                    metadata={"metric_id": metric.id}
                )
                self.db.add(history)
                self.db.commit()

    async def create_alert(self, alert: AlertCreate) -> Alert:
        db_alert = Alert(
            metric_name=alert.metric_name,
            condition=alert.condition,
            threshold=alert.threshold,
            severity=alert.severity,
            status="active",
            metadata=alert.metadata
        )
        self.db.add(db_alert)
        self.db.commit()
        self.db.refresh(db_alert)
        return db_alert

    async def update_alert(self, alert_id: int, alert_update: AlertUpdate) -> Alert:
        db_alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if not db_alert:
            raise ValueError(f"Alert with id {alert_id} not found")
            
        if alert_update.status:
            db_alert.status = alert_update.status
            if alert_update.status == "resolved":
                db_alert.resolved_at = datetime.utcnow()
                
        if alert_update.metadata:
            db_alert.metadata = alert_update.metadata
            
        self.db.commit()
        self.db.refresh(db_alert)
        return db_alert

    async def get_metrics(
        self,
        name: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Metric]:
        query = self.db.query(Metric)
        
        if name:
            query = query.filter(Metric.name == name)
        if start_time:
            query = query.filter(Metric.timestamp >= start_time)
        if end_time:
            query = query.filter(Metric.timestamp <= end_time)
            
        return query.order_by(Metric.timestamp.desc()).all()

    async def get_alerts(
        self,
        status: Optional[str] = None,
        severity: Optional[str] = None
    ) -> List[Alert]:
        query = self.db.query(Alert)
        
        if status:
            query = query.filter(Alert.status == status)
        if severity:
            query = query.filter(Alert.severity == severity)
            
        return query.order_by(Alert.created_at.desc()).all()

    async def get_alert_history(
        self,
        alert_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[AlertHistory]:
        query = self.db.query(AlertHistory).filter(AlertHistory.alert_id == alert_id)
        
        if start_time:
            query = query.filter(AlertHistory.timestamp >= start_time)
        if end_time:
            query = query.filter(AlertHistory.timestamp <= end_time)
            
        return query.order_by(AlertHistory.timestamp.desc()).all()

    async def get_monitoring_summary(self) -> MonitoringSummary:
        # Общее количество метрик
        total_metrics = self.db.query(func.count(Metric.id)).scalar()
        
        # Статистика по алертам
        alerts = self.db.query(
            Alert.status,
            Alert.severity,
            func.count(Alert.id)
        ).group_by(
            Alert.status,
            Alert.severity
        ).all()
        
        active_alerts = sum(count for status, _, count in alerts if status == "active")
        critical_alerts = sum(count for _, severity, count in alerts if severity == "critical")
        warning_alerts = sum(count for _, severity, count in alerts if severity == "warning")
        info_alerts = sum(count for _, severity, count in alerts if severity == "info")
        
        # Метрики по имени
        metrics_by_name = dict(self.db.query(
            Metric.name,
            func.count(Metric.id)
        ).group_by(Metric.name).all())
        
        # Алерты по серьезности
        alerts_by_severity = dict(self.db.query(
            Alert.severity,
            func.count(Alert.id)
        ).group_by(Alert.severity).all())
        
        return MonitoringSummary(
            total_metrics=total_metrics,
            active_alerts=active_alerts,
            critical_alerts=critical_alerts,
            warning_alerts=warning_alerts,
            info_alerts=info_alerts,
            metrics_by_name=metrics_by_name,
            alerts_by_severity=alerts_by_severity
        ) 