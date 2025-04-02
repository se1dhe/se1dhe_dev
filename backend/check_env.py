from app.core.env import settings

print("Database Configuration:")
print(f"MYSQL_USER: {settings.MYSQL_USER}")
print(f"MYSQL_PASSWORD: {settings.MYSQL_PASSWORD}")
print(f"MYSQL_HOST: {settings.MYSQL_HOST}")
print(f"MYSQL_PORT: {settings.MYSQL_PORT}")
print(f"MYSQL_DB: {settings.MYSQL_DB}")
print(f"\nSQLALCHEMY_DATABASE_URI: {settings.SQLALCHEMY_DATABASE_URI}")

print("\nAdmin Credentials:")
print(f"ADMIN_USERNAME: {settings.ADMIN_USERNAME}")
print(f"ADMIN_PASSWORD: {settings.ADMIN_PASSWORD}") 