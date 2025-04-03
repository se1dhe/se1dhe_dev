# 🎨 Административная панель

<div align="center">

![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0.0-blue.svg)
![Material-UI](https://img.shields.io/badge/Material--UI-5.0.0-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Современная административная панель с красивым интерфейсом и мощным функционалом

[Демо](https://demo.example.com) • [Документация](https://docs.example.com) • [Поддержка](https://support.example.com)

</div>

## 📋 Содержание

- [✨ Особенности](#-особенности)
- [🚀 Быстрый старт](#-быстрый-старт)
- [📦 Установка](#-установка)
- [💻 Разработка](#-разработка)
- [🏗️ Архитектура](#️-архитектура)
- [🔐 Аутентификация](#-аутентификация)
- [🎨 Кастомизация](#-кастомизация)
- [🤝 Участие в разработке](#-участие-в-разработке)
- [📝 Лицензия](#-лицензия)
- [👥 Команда](#-команда)

## ✨ Особенности

<table>
<tr>
<td width="50%">

### 🎨 Интерфейс
- Современный тёмный дизайн
- Плавные анимации и переходы
- Адаптивная верстка
- Кастомные компоненты Material-UI

</td>
<td width="50%">

### 🔒 Безопасность
- JWT аутентификация
- Ролевой доступ
- Защищенные маршруты
- Двухфакторная аутентификация

</td>
</tr>
<tr>
<td width="50%">

### ⚡ Производительность
- Быстрая загрузка
- Оптимизированный бандл
- Кэширование данных
- Ленивая загрузка

</td>
<td width="50%">

### 🛠️ Разработка
- TypeScript
- Vite
- ESLint + Prettier
- Husky + lint-staged

</td>
</tr>
</table>

## 🚀 Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/yourusername/admin-dashboard.git

# Переход в директорию проекта
cd admin-dashboard

# Установка зависимостей
npm install

# Запуск сервера разработки
npm run dev
```

## 📦 Установка

### Предварительные требования

- Node.js >= 14
- npm >= 7
- Git

### Шаги установки

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/yourusername/admin-dashboard.git
   ```

2. **Установка зависимостей**
   ```bash
   npm install
   ```

3. **Настройка переменных окружения**
   ```bash
   cp .env.example .env
   ```

4. **Запуск приложения**
   ```bash
   npm run dev
   ```

## 💻 Разработка

### Доступные скрипты

```bash
# Запуск сервера разработки
npm run dev

# Сборка для продакшена
npm run build

# Запуск линтера
npm run lint

# Запуск тестов
npm run test

# Проверка типов
npm run type-check
```

### Структура проекта

```
src/
├── assets/        # Статические ресурсы
├── components/    # Переиспользуемые компоненты
├── contexts/      # React контексты
├── hooks/         # Кастомные хуки
├── layouts/       # Шаблоны страниц
├── pages/         # Компоненты страниц
├── services/      # API сервисы
├── store/         # Управление состоянием
├── theme/         # Конфигурация темы
├── types/         # TypeScript типы
└── utils/         # Вспомогательные функции
```

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

## 🎨 Кастомизация

### Тема

Настройка темы в `src/theme/theme.ts`:

```typescript
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f50057',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});
```

### Компоненты

Все компоненты Material-UI можно кастомизировать через:

- Переопределение стилей
- Создание собственных компонентов
- Использование styled-components

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку для функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Добавлена удивительная функция'`)
4. Отправьте изменения в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

### Правила коммитов

- feat: Новая функция
- fix: Исправление бага
- docs: Изменения в документации
- style: Форматирование кода
- refactor: Рефакторинг кода
- test: Добавление тестов
- chore: Обновление зависимостей

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

- [Material-UI](https://mui.com/) за прекрасные компоненты
- [Framer Motion](https://www.framer.com/motion/) за отличные анимации
- [React Router](https://reactrouter.com/) за маршрутизацию
- [TypeScript](https://www.typescriptlang.org/) за типизацию
- [Vite](https://vitejs.dev/) за быструю разработку

---

<div align="center">

Сделано с ❤️ командой разработчиков

</div>
