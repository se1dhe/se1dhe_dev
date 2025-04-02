from typing import List, Optional, Dict, Any, Union, Tuple
from datetime import datetime, date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract, desc
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import Date

from app.models.metric import Metric
from app.schemas.metric import MetricCreate, MetricQuery
from .base import CRUDBase


class CRUDMetric(CRUDBase[Metric, MetricCreate, None]):
    """CRUD операции для метрик"""
    
    def create_metric(
        self, db: Session, *, name: str, value: float, dimensions: Optional[Dict[str, Any]] = None
    ) -> Metric:
        """
        Создать новую метрику
        
        Args:
            db: Сессия БД
            name: Название метрики
            value: Значение метрики
            dimensions: Дополнительные измерения (опционально)
            
        Returns:
            Созданная метрика
        """
        db_obj = Metric(
            name=name,
            value=value,
            dimensions=dimensions,
            timestamp=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_name(
        self, db: Session, *, name: str, skip: int = 0, limit: int = 100
    ) -> List[Metric]:
        """
        Получить метрики по имени
        
        Args:
            db: Сессия БД
            name: Название метрики
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список метрик с заданным именем
        """
        return (
            db.query(Metric)
            .filter(Metric.name == name)
            .order_by(desc(Metric.timestamp))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_time_range(
        self, db: Session, *, start_date: datetime, end_date: datetime, 
        name: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[Metric]:
        """
        Получить метрики за определенный период времени
        
        Args:
            db: Сессия БД
            start_date: Начальная дата
            end_date: Конечная дата
            name: Название метрики (опционально)
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
            
        Returns:
            Список метрик за указанный период
        """
        query = db.query(Metric).filter(
            Metric.timestamp >= start_date,
            Metric.timestamp <= end_date
        )
        
        if name:
            query = query.filter(Metric.name == name)
            
        return (
            query
            .order_by(desc(Metric.timestamp))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def query_metrics(
        self, db: Session, *, query: MetricQuery
    ) -> List[Dict[str, Any]]:
        """
        Выполнить сложный запрос метрик с группировкой
        
        Args:
            db: Сессия БД
            query: Параметры запроса
            
        Returns:
            Список результатов с агрегированными данными
        """
        # Базовый запрос
        db_query = db.query(Metric).filter(Metric.name == query.name)
        
        # Добавляем временной диапазон, если указан
        if query.start_date:
            db_query = db_query.filter(Metric.timestamp >= query.start_date)
        if query.end_date:
            db_query = db_query.filter(Metric.timestamp <= query.end_date)
        
        # Добавляем фильтры по измерениям, если указаны
        if query.dimensions:
            for key, value in query.dimensions.items():
                # Фильтруем по значению в JSON-поле
                db_query = db_query.filter(
                    Metric.dimensions[key].astext == str(value)
                )
        
        # Если запрос без группировки, просто возвращаем метрики
        if not query.group_by:
            metrics = db_query.order_by(desc(Metric.timestamp)).limit(query.limit).all()
            return [
                {
                    "id": m.id,
                    "name": m.name,
                    "value": m.value,
                    "dimensions": m.dimensions or {},
                    "timestamp": m.timestamp
                }
                for m in metrics
            ]
        
        # Иначе выполняем агрегацию
        group_fields = []
        for field in query.group_by:
            if field == 'timestamp':
                # Группируем по дате
                group_fields.append(cast(Metric.timestamp, Date).label('date'))
            else:
                # Группируем по измерению
                group_fields.append(Metric.dimensions[field].astext.label(field))
        
        # Агрегация по группам
        result_query = db.query(
            *group_fields,
            func.avg(Metric.value).label('avg_value'),
            func.sum(Metric.value).label('sum_value'),
            func.min(Metric.value).label('min_value'),
            func.max(Metric.value).label('max_value'),
            func.count().label('count')
        ).filter(Metric.name == query.name)
        
        # Добавляем временной диапазон, если указан
        if query.start_date:
            result_query = result_query.filter(Metric.timestamp >= query.start_date)
        if query.end_date:
            result_query = result_query.filter(Metric.timestamp <= query.end_date)
        
        # Добавляем фильтры по измерениям, если указаны
        if query.dimensions:
            for key, value in query.dimensions.items():
                result_query = result_query.filter(
                    Metric.dimensions[key].astext == str(value)
                )
        
        # Группировка и ограничение результатов
        result = result_query.group_by(*group_fields).limit(query.limit).all()
        
        # Преобразуем результаты в словари
        return [dict(zip(r.keys(), r)) for r in result]
    
    def get_last_value(
        self, db: Session, *, name: str, dimensions: Optional[Dict[str, Any]] = None
    ) -> Optional[float]:
        """
        Получить последнее значение метрики
        
        Args:
            db: Сессия БД
            name: Название метрики
            dimensions: Дополнительные измерения (опционально)
            
        Returns:
            Последнее значение метрики или None
        """
        query = db.query(Metric).filter(Metric.name == name)
        
        if dimensions:
            for key, value in dimensions.items():
                query = query.filter(
                    Metric.dimensions[key].astext == str(value)
                )
        
        metric = query.order_by(desc(Metric.timestamp)).first()
        return metric.value if metric else None


# Создание экземпляра CRUD для использования в API
metric = CRUDMetric(Metric) 