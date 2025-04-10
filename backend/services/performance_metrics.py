from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from ..models.monitoring import Metric
from ..schemas.monitoring import MetricCreate
from ..services.monitoring_service import MonitoringService
import psutil
import time
import gc

class PerformanceMetricsService:
    def __init__(self, db: Session):
        self.db = db
        self.monitoring_service = MonitoringService(db)
        self._last_collection = datetime.utcnow()

    async def collect_system_metrics(self) -> None:
        """Сбор системных метрик"""
        # CPU метрики
        cpu_percent = psutil.cpu_percent(interval=1)
        await self._record_metric("system.cpu.percent", cpu_percent)
        
        # Memory метрики
        memory = psutil.virtual_memory()
        await self._record_metric("system.memory.percent", memory.percent)
        await self._record_metric("system.memory.used", memory.used / (1024 * 1024))  # MB
        await self._record_metric("system.memory.available", memory.available / (1024 * 1024))  # MB
        
        # Disk метрики
        disk = psutil.disk_usage('/')
        await self._record_metric("system.disk.percent", disk.percent)
        await self._record_metric("system.disk.used", disk.used / (1024 * 1024 * 1024))  # GB
        await self._record_metric("system.disk.free", disk.free / (1024 * 1024 * 1024))  # GB

    async def collect_application_metrics(self) -> None:
        """Сбор метрик приложения"""
        # GC метрики
        gc.collect()
        gc_stats = gc.get_stats()
        await self._record_metric("app.gc.collections", sum(stat['collections'] for stat in gc_stats))
        await self._record_metric("app.gc.collected", sum(stat['collected'] for stat in gc_stats))
        
        # Python memory
        process = psutil.Process()
        memory_info = process.memory_info()
        await self._record_metric("app.memory.rss", memory_info.rss / (1024 * 1024))  # MB
        await self._record_metric("app.memory.vms", memory_info.vms / (1024 * 1024))  # MB

    async def collect_database_metrics(self) -> None:
        """Сбор метрик базы данных"""
        # Количество активных соединений
        active_connections = self.db.execute("SHOW STATUS LIKE 'Threads_connected'").scalar()
        await self._record_metric("db.connections.active", active_connections)
        
        # Время выполнения запросов
        query_time = self.db.execute("SHOW STATUS LIKE 'Uptime'").scalar()
        await self._record_metric("db.uptime", query_time)

    async def collect_api_metrics(self, endpoint: str, method: str, duration: float, status_code: int) -> None:
        """Сбор метрик API"""
        await self._record_metric(
            "api.request.duration",
            duration,
            labels={"endpoint": endpoint, "method": method, "status_code": str(status_code)}
        )
        await self._record_metric(
            "api.request.count",
            1,
            labels={"endpoint": endpoint, "method": method, "status_code": str(status_code)}
        )

    async def collect_cache_metrics(self, operation: str, duration: float, success: bool) -> None:
        """Сбор метрик кэша"""
        await self._record_metric(
            "cache.operation.duration",
            duration,
            labels={"operation": operation, "success": str(success)}
        )
        await self._record_metric(
            "cache.operation.count",
            1,
            labels={"operation": operation, "success": str(success)}
        )

    async def collect_all_metrics(self) -> None:
        """Сбор всех метрик"""
        start_time = time.time()
        
        try:
            await self.collect_system_metrics()
            await self.collect_application_metrics()
            await self.collect_database_metrics()
            
            # Записываем время сбора метрик
            collection_duration = time.time() - start_time
            await self._record_metric("metrics.collection.duration", collection_duration)
            
            self._last_collection = datetime.utcnow()
            
        except Exception as e:
            await self._record_metric(
                "metrics.collection.error",
                1,
                labels={"error": str(e)}
            )

    async def _record_metric(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, Any]] = None
    ) -> None:
        """Запись метрики в базу данных"""
        metric = MetricCreate(
            name=name,
            value=value,
            labels=labels or {},
            metadata={"timestamp": datetime.utcnow().isoformat()}
        )
        await self.monitoring_service.record_metric(metric) 