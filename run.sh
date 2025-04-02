#!/bin/bash

# Запуск бэкенда
cd backend && python run.py &

# Запуск фронтенда
cd ../frontend && npm run dev &

# Ожидание завершения всех процессов
wait 