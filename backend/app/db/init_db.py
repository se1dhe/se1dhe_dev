import logging
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.core.security import get_password_hash
from backend.app.models.user import User
from backend.app.models.category import Category
from backend.app.models.bot import Bot

logger = logging.getLogger(__name__)


def create_first_superuser(db: Session) -> None:
    """Создает суперпользователя, если его еще нет в базе"""
    user = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if not user:
        user_in = User(
            email=settings.ADMIN_EMAIL,
            username="admin",
            hashed_password=get_password_hash("admin"),  # Заменить на реальный пароль
            is_superuser=True,
            full_name="Admin User",
        )
        db.add(user_in)
        db.commit()
        logger.info(f"Superuser {settings.ADMIN_EMAIL} created")
    else:
        logger.info(f"Superuser {settings.ADMIN_EMAIL} already exists")


def create_initial_categories(db: Session) -> None:
    """Создает начальные категории для ботов"""
    categories = [
        {
            "name": "Информационные боты",
            "description": "Боты для получения информации из различных источников",
            "slug": "info-bots",
            "image_url": "/assets/images/categories/info-bots.jpg",
        },
        {
            "name": "Управление задачами",
            "description": "Боты для управления задачами и проектами",
            "slug": "task-management-bots",
            "image_url": "/assets/images/categories/task-bots.jpg",
        },
        {
            "name": "Уведомления и оповещения",
            "description": "Боты для отправки уведомлений и оповещений",
            "slug": "notification-bots",
            "image_url": "/assets/images/categories/notification-bots.jpg",
        },
    ]

    for category_data in categories:
        category = db.query(Category).filter(Category.slug == category_data["slug"]).first()
        if not category:
            category = Category(**category_data)
            db.add(category)
            db.commit()
            logger.info(f"Category {category_data['name']} created")
        else:
            logger.info(f"Category {category_data['name']} already exists")


def create_sample_bots(db: Session) -> None:
    """Создает несколько примеров ботов для демонстрации"""
    # Получаем категории
    info_category = db.query(Category).filter(Category.slug == "info-bots").first()
    task_category = db.query(Category).filter(Category.slug == "task-management-bots").first()
    notif_category = db.query(Category).filter(Category.slug == "notification-bots").first()

    if not all([info_category, task_category, notif_category]):
        logger.warning("Cannot create sample bots: categories not found")
        return

    bots = [
        {
            "name": "Новостной бот",
            "slug": "news-bot",
            "short_description": "Бот для получения последних новостей",
            "full_description": "Настраиваемый бот для получения новостей из различных источников по выбранным темам.",
            "price": 1500.0,
            "category_id": info_category.id,
            "features": ["Настраиваемые источники новостей", "Фильтрация по темам", "Регулярная отправка дайджестов"],
            "preview_image_url": "/assets/images/bots/news-bot.jpg",
        },
        {
            "name": "Менеджер задач",
            "slug": "task-manager-bot",
            "short_description": "Бот для управления личными задачами",
            "full_description": "Удобный бот для создания, отслеживания и управления вашими задачами прямо в Telegram.",
            "price": 2000.0,
            "category_id": task_category.id,
            "features": ["Создание задач", "Напоминания", "Категоризация", "Отметка выполненных задач"],
            "preview_image_url": "/assets/images/bots/task-bot.jpg",
        },
        {
            "name": "Бот-напоминалка",
            "slug": "reminder-bot",
            "short_description": "Бот для установки напоминаний",
            "full_description": "Бот позволяет устанавливать напоминания на определенное время и отправляет уведомления.",
            "price": 1200.0,
            "category_id": notif_category.id,
            "features": ["Гибкая настройка времени", "Повторяющиеся напоминания", "Разные уровни приоритета"],
            "preview_image_url": "/assets/images/bots/reminder-bot.jpg",
        },
    ]

    for bot_data in bots:
        bot = db.query(Bot).filter(Bot.slug == bot_data["slug"]).first()
        if not bot:
            bot = Bot(**bot_data)
            db.add(bot)
            db.commit()
            logger.info(f"Bot {bot_data['name']} created")
        else:
            logger.info(f"Bot {bot_data['name']} already exists")


def init_db(db: Session) -> None:
    """Инициализирует базу данных начальными данными"""
    try:
        # Создаем суперпользователя
        create_first_superuser(db)

        # Создаем начальные категории
        create_initial_categories(db)

        # Создаем примеры ботов
        create_sample_bots(db)

        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise