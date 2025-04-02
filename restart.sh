#!/bin/bash

# Остановка процессов на портах 8000 и 3000/3001
echo "Stopping existing servers..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:3001 | xargs kill -9 2>/dev/null

# Остановка всех процессов Python
echo "Stopping all Python processes..."
pkill -9 python 2>/dev/null
pkill -9 -f "python.*run.py" 2>/dev/null
pkill -9 -f "python.*telegram_bot.py" 2>/dev/null
sleep 5  # Увеличиваем время ожидания

# Проверка, что все процессы Python остановлены
if pgrep -f "python" > /dev/null; then
    echo "Warning: Some Python processes are still running"
    pgrep -fl "python"
fi

# Запуск бэкенда
echo "Starting backend server..."
cd backend && python run.py &

# Запуск фронтенда
echo "Starting frontend server..."
cd frontend && npm run dev &

# Ожидание завершения всех процессов
wait 