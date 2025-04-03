import uvicorn
import os

if __name__ == "__main__":
    # Получаем абсолютный путь к директории app
    app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[app_dir]
    ) 