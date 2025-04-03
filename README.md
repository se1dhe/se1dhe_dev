# 🚀 SE1DHE - Система управления предприятием

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0.0-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue.svg)
![Aiogram](https://img.shields.io/badge/Aiogram-3.0.0-blue.svg)

Современная система управления предприятием с веб-интерфейсом и Telegram ботом

[Документация](https://docs.example.com) • [Поддержка](https://support.example.com)

</div>

## 📋 Содержание

- [✨ Особенности](#-особенности)
- [🏗️ Архитектура](#️-архитектура)
- [🚀 Быстрый старт](#-быстрый-старт)
- [📦 Установка](#-установка)
- [💻 Разработка](#-разработка)
- [🔐 Аутентификация](#-аутентификация)
- [🤖 Telegram бот](#-telegram-бот)
- [📝 Лицензия](#-лицензия)
- [👥 Команда](#-команда)

## ✨ Особенности

<table>
<tr>
<td width="50%">

### 🎨 Frontend
- Современный React + TypeScript
- Material-UI компоненты
- Адаптивный дизайн
- Анимации с Framer Motion

</td>
<td width="50%">

### 🔧 Backend
- FastAPI + Python
- MySQL база данных
- JWT аутентификация
- RESTful API

</td>
</tr>
<tr>
<td width="50%">

### 🤖 Telegram
- Aiogram 3.0
- Интеграция с основным приложением
- Уведомления и оповещения
- Управление через бота

</td>
<td width="50%">

### 📊 Функционал
- Управление пользователями
- Аналитика и отчеты
- Мониторинг системы
- Логирование действий

</td>
</tr>
</table>

## 🏗️ Архитектура

```
project/
├── frontend/          # React приложение
│   ├── src/          # Исходный код
│   ├── public/       # Статические файлы
│   └── package.json  # Зависимости
├── backend/          # FastAPI сервер
│   ├── app/         # Исходный код
│   ├── tests/       # Тесты
│   └── requirements.txt  # Зависимости
├── bot/             # Telegram бот
│   ├── handlers/    # Обработчики команд
│   ├── keyboards/   # Клавиатуры
│   └── config.py    # Конфигурация
└── docs/            # Документация
```

## 🚀 Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/yourusername/se1dhe.git

# Переход в директорию проекта
cd se1dhe

# Запуск скрипта установки
./run.sh
```

## 📦 Установка

### Предварительные требования

- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Git

### Шаги установки

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/yourusername/se1dhe.git
   cd se1dhe
   ```

2. **Настройка окружения**
   ```bash
   # Создание виртуального окружения
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   .\venv\Scripts\activate  # Windows

   # Установка зависимостей
   pip install -r backend/requirements.txt
   cd frontend && npm install
   ```

3. **Настройка базы данных**
   ```bash
   # Создание базы данных
   mysql -u root -p
   CREATE DATABASE se1dhe CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   # Применение миграций
   cd backend
   alembic upgrade head
   ```

4. **Настройка Telegram бота**
   ```bash
   # Копирование конфигурации
   cp bot/config.example.py bot/config.py
   # Отредактируйте config.py и добавьте ваш токен бота
   ```

5. **Запуск приложения**
   ```bash
   # Запуск бэкенда
   cd backend
   uvicorn app.main:app --reload

   # Запуск фронтенда
   cd frontend
   npm run dev

   # Запуск бота
   cd bot
   python main.py
   ```

## 💻 Разработка

### Скрипты

```bash
# Запуск всего приложения
./run.sh

# Перезапуск приложения
./restart.sh

# Запуск тестов
cd backend && pytest
cd frontend && npm test

# Линтинг
cd backend && flake8
cd frontend && npm run lint
```

### Структура разработки

- **Frontend**: React + TypeScript + Material-UI
- **Backend**: FastAPI + SQLAlchemy + Alembic
- **База данных**: MySQL
- **Telegram**: Aiogram 3.0
- **Тестирование**: pytest + React Testing Library

## 🔐 Аутентификация

### Роли пользователей

- 👑 **Администратор**
  - Полный доступ ко всем функциям
  - Управление пользователями
  - Настройка системы

- 👤 **Пользователь**
  - Базовый доступ
  - Просмотр данных
  - Личный профиль

### Процесс входа

1. Ввод email и пароля
2. Валидация данных
3. Получение JWT токена
4. Сохранение в localStorage
5. Перенаправление на дашборд

## 🤖 Telegram бот

### Функции бота

- 📊 Получение статистики
- 🔔 Уведомления о событиях
- 👥 Управление пользователями
- ⚙️ Настройка системы

### Команды

- `/start` - Начало работы
- `/help` - Справка
- `/stats` - Статистика
- `/settings` - Настройки

## 📝 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для подробностей.

## 👥 Команда

<table>
<tr>
<td align="center">
<a href="https://github.com/yourusername">
<img src="https://avatars.githubusercontent.com/yourusername" width="100px;" alt=""/>
<br />
<sub><b>Ваше имя</b></sub>
</a>
<br />
<sub>Lead Developer</sub>
</td>
</tr>
</table>

## 🙏 Благодарности

- [FastAPI](https://fastapi.tiangolo.com/) за отличный фреймворк
- [React](https://reactjs.org/) за прекрасную библиотеку
- [Material-UI](https://mui.com/) за компоненты
- [MySQL](https://www.mysql.com/) за надежную БД
- [Aiogram](https://docs.aiogram.dev/) за удобный фреймворк для ботов

---

<div align="center">

Сделано с ❤️ командой разработчиков

</div> 