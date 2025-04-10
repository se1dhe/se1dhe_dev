# Используем официальный образ Python
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt setup.py ./

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install -e .

# Копирование исходного кода
COPY . .

# Создание директорий для логов
RUN mkdir -p logs

# Установка прав на выполнение скриптов
RUN chmod +x docker-start.sh

# Открытие портов
EXPOSE 8000 3000

# Запуск приложения
CMD ["./docker-start.sh"] 