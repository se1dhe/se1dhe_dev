#!/bin/bash

# Функция для проверки запущен ли контейнер
check_container() {
    docker ps | grep $1 > /dev/null
    return $?
}

# Функция для обновления URL ngrok в .env
update_ngrok_url() {
    # Ждем пока ngrok запустится и получит URL
    sleep 5
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o "https://[0-9a-z]*\.ngrok\.io")
    if [ ! -z "$NGROK_URL" ]; then
        sed -i.bak "s|NGROK_URL=.*|NGROK_URL=$NGROK_URL|" .env
        echo "Updated NGROK_URL in .env to: $NGROK_URL"
    fi
}

# Проверяем и перезапускаем контейнеры если нужно
if check_container "se1dhe_dev_app"; then
    echo "Restarting existing containers..."
    docker-compose down
    docker-compose up -d
else
    echo "Starting new containers..."
    docker-compose up -d
fi

# Запускаем ngrok в фоновом режиме
ngrok http 8000 --region=${NGROK_REGION} --log=stdout > /app/logs/ngrok.log 2>&1 &

# Обновляем URL ngrok в .env
update_ngrok_url

# Запускаем основные сервисы
echo "Starting backend services..."
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload > /app/logs/backend.log 2>&1 &

echo "Starting frontend services..."
cd ../frontend && npm run serve > /app/logs/frontend.log 2>&1 &

echo "Starting Telegram bot..."
cd ../bot && python main.py > /app/logs/bot.log 2>&1 &

# Ждем завершения всех процессов
wait 