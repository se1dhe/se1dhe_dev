import os
import json

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def create_file(path, content=""):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created file: {path}")

def create_init_file(path):
    create_file(os.path.join(path, "__init__.py"))

def main():
    # Project root structure
    root_dirs = [
        "backend",
        "frontend",
        "scripts",
        "docs"
    ]
    
    for dir_name in root_dirs:
        create_directory(dir_name)
        create_init_file(dir_name)

    # Backend structure
    backend_dirs = [
        "backend/app",
        "backend/app/api",
        "backend/app/core",
        "backend/app/db",
        "backend/app/models",
        "backend/app/schemas",
        "backend/app/services",
        "backend/app/utils",
        "backend/app/websocket",
        "backend/tests",
        "backend/alembic"
    ]

    for dir_name in backend_dirs:
        create_directory(dir_name)
        create_init_file(dir_name)

    # Frontend structure
    frontend_dirs = [
        "frontend/src",
        "frontend/src/assets",
        "frontend/src/components",
        "frontend/src/views",
        "frontend/src/router",
        "frontend/src/store",
        "frontend/src/api",
        "frontend/src/utils",
        "frontend/src/locales",
        "frontend/public"
    ]

    for dir_name in frontend_dirs:
        create_directory(dir_name)
        if "src" in dir_name:
            create_init_file(dir_name)

    # Create main backend files
    backend_files = {
        "backend/requirements.txt": "",
        "backend/main.py": "",
        "backend/.env.example": "",
        "backend/alembic.ini": "",
        "backend/app/core/config.py": "",
        "backend/app/core/security.py": "",
        "backend/app/db/base.py": "",
        "backend/app/db/session.py": "",
        "backend/app/api/api.py": "",
        "backend/app/api/endpoints/auth.py": "",
        "backend/app/api/endpoints/bots.py": "",
        "backend/app/api/endpoints/users.py": "",
        "backend/app/api/endpoints/orders.py": "",
        "backend/app/api/endpoints/notifications.py": "",
        "backend/app/models/user.py": "",
        "backend/app/models/bot.py": "",
        "backend/app/models/order.py": "",
        "backend/app/models/notification.py": "",
        "backend/app/schemas/user.py": "",
        "backend/app/schemas/bot.py": "",
        "backend/app/schemas/order.py": "",
        "backend/app/schemas/notification.py": "",
        "backend/app/services/auth.py": "",
        "backend/app/services/bot.py": "",
        "backend/app/services/order.py": "",
        "backend/app/services/notification.py": "",
        "backend/app/websocket/manager.py": "",
        "backend/app/websocket/events.py": ""
    }

    for file_path, content in backend_files.items():
        create_file(file_path, content)

    # Create main frontend files
    frontend_files = {
        "frontend/package.json": "",
        "frontend/vue.config.js": "",
        "frontend/.env.example": "",
        "frontend/src/main.js": "",
        "frontend/src/App.vue": "",
        "frontend/src/router/index.js": "",
        "frontend/src/store/index.js": "",
        "frontend/src/api/auth.js": "",
        "frontend/src/api/bots.js": "",
        "frontend/src/api/orders.js": "",
        "frontend/src/api/notifications.js": "",
        "frontend/src/components/layout/Header.vue": "",
        "frontend/src/components/layout/Footer.vue": "",
        "frontend/src/components/layout/Sidebar.vue": "",
        "frontend/src/views/Home.vue": "",
        "frontend/src/views/Bots.vue": "",
        "frontend/src/views/BotDetail.vue": "",
        "frontend/src/views/Profile.vue": "",
        "frontend/src/views/Admin.vue": "",
        "frontend/src/locales/ru.json": "",
        "frontend/src/locales/en.json": ""
    }

    for file_path, content in frontend_files.items():
        create_file(file_path, content)

    # Create documentation files
    docs_files = {
        "docs/README.md": "",
        "docs/API.md": "",
        "docs/DEPLOYMENT.md": "",
        "docs/CONTRIBUTING.md": ""
    }

    for file_path, content in docs_files.items():
        create_file(file_path, content)

    # Create root level files
    root_files = {
        "README.md": "",
        "TODO.md": "",
        ".gitignore": "",
        ".env.example": ""
    }

    for file_path, content in root_files.items():
        create_file(file_path, content)

    print("\nProject structure created successfully!")

if __name__ == "__main__":
    main() 