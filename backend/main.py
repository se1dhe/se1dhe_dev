import os
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    import routers

    # Настройка логгера
    log_dir = os.getenv("LOG_DIR", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Настройка формата логирования
    log_format = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format=log_format,
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "backend.log")),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)

    app = FastAPI(
        title="Se1dhe Dev API",
        description="API для e-commerce платформы продажи Telegram ботов",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=eval(os.getenv("CORS_ORIGINS", "[]")),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Монтирование статических файлов
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Включение всех роутеров
    app.include_router(routers.router, prefix="/api")

    @app.get("/")
    async def root():
        logger.info("Root endpoint called")
        return {"message": "Welcome to Se1dhe Dev API"}

    @app.get("/health")
    async def health_check():
        logger.info("Health check endpoint called")
        return {"status": "healthy"}

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=int(os.getenv("BACKEND_PORT", 8000)),
            reload=True
        )
except Exception as e:
    print(f"Error during startup: {str(e)}")
    raise 