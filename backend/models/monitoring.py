from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    labels = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False)
    condition = Column(String(50), nullable=False)  # 'gt', 'lt', 'eq', 'neq'
    threshold = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False)  # 'info', 'warning', 'critical'
    status = Column(String(20), nullable=False)  # 'active', 'resolved'
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    metadata = Column(JSON, nullable=True)

class AlertHistory(Base):
    __tablename__ = "alert_history"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=False)
    metric_value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)

    alert = relationship("Alert", back_populates="history") 