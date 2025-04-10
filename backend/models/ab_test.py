from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum

class ABTestStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"

class ABTestType(enum.Enum):
    UI_CHANGES = "ui_changes"
    PRICING = "pricing"
    FEATURES = "features"
    CONTENT = "content"
    PROMOTIONS = "promotions"

class ABTest(Base):
    __tablename__ = "ab_tests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(ABTestType), nullable=False)
    status = Column(Enum(ABTestStatus), default=ABTestStatus.DRAFT)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    target_audience = Column(JSON, nullable=True)  # Критерии для выбора участников
    variants = Column(JSON, nullable=False)  # Описания вариантов теста
    metrics = Column(JSON, nullable=False)  # Метрики для измерения
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    results = relationship("ABTestResult", back_populates="test")

    def __repr__(self):
        return f"<ABTest {self.id} - {self.name}>"

class ABTestResult(Base):
    __tablename__ = "ab_test_results"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("ab_tests.id"), nullable=False)
    variant = Column(String(50), nullable=False)  # Название варианта
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    metrics_data = Column(JSON, nullable=False)  # Результаты по метрикам
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    test = relationship("ABTest", back_populates="results")
    user = relationship("User", back_populates="ab_test_results")

    def __repr__(self):
        return f"<ABTestResult {self.id} - Test {self.test_id}>" 