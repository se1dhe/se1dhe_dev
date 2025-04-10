from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MetricCondition(str, Enum):
    GREATER_THAN = "gt"
    LESS_THAN = "lt"
    EQUAL = "eq"
    NOT_EQUAL = "neq"

class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class AlertStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"

class MetricBase(BaseModel):
    name: str = Field(..., max_length=100)
    value: float
    labels: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class MetricCreate(MetricBase):
    pass

class MetricInDB(MetricBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class MetricResponse(MetricInDB):
    pass

class AlertBase(BaseModel):
    metric_name: str = Field(..., max_length=100)
    condition: MetricCondition
    threshold: float
    severity: AlertSeverity
    metadata: Optional[Dict[str, Any]] = None

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    status: Optional[AlertStatus] = None
    metadata: Optional[Dict[str, Any]] = None

class AlertInDB(AlertBase):
    id: int
    status: AlertStatus
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AlertResponse(AlertInDB):
    pass

class AlertHistoryBase(BaseModel):
    alert_id: int
    metric_value: float
    metadata: Optional[Dict[str, Any]] = None

class AlertHistoryCreate(AlertHistoryBase):
    pass

class AlertHistoryInDB(AlertHistoryBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class AlertHistoryResponse(AlertHistoryInDB):
    pass

class MonitoringSummary(BaseModel):
    total_metrics: int
    active_alerts: int
    critical_alerts: int
    warning_alerts: int
    info_alerts: int
    metrics_by_name: Dict[str, int]
    alerts_by_severity: Dict[str, int] 