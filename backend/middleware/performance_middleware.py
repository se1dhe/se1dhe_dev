from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from datetime import datetime
import time
from ..database import get_db
from ..services.performance_metrics import PerformanceMetricsService

class PerformanceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.db = next(get_db())
        self.metrics_service = PerformanceMetricsService(self.db)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Собираем метрики API
            await self.metrics_service.collect_api_metrics(
                endpoint=str(request.url.path),
                method=request.method,
                duration=duration,
                status_code=response.status_code
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            # Собираем метрики для ошибок
            await self.metrics_service.collect_api_metrics(
                endpoint=str(request.url.path),
                method=request.method,
                duration=duration,
                status_code=500
            )
            
            raise e 