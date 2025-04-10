from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from loguru import logger
import time
import json

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        # Засекаем время начала обработки запроса
        start_time = time.time()
        
        # Получаем тело запроса
        body = await request.body()
        if body:
            try:
                body = json.loads(body)
            except:
                body = body.decode()
        
        # Логируем входящий запрос
        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "body": body,
                "client": request.client.host if request.client else None,
            }
        )
        
        # Обрабатываем запрос
        response = await call_next(request)
        
        # Засекаем время окончания обработки запроса
        process_time = time.time() - start_time
        
        # Логируем ответ
        logger.info(
            f"Outgoing response: {response.status_code}",
            extra={
                "status_code": response.status_code,
                "process_time": process_time,
                "headers": dict(response.headers),
            }
        )
        
        return response

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            return Response(
                content=json.dumps({"detail": "Internal server error"}),
                status_code=500,
                media_type="application/json"
            )

class CORSMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, allow_origins: list = None):
        super().__init__(app)
        self.allow_origins = allow_origins or []
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Добавляем CORS заголовки
        origin = request.headers.get("origin")
        if origin in self.allow_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
        return response 