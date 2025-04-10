from .database import Base, engine, get_db
from . import models, schemas, crud

# Создание таблиц базы данных
def init_db():
    Base.metadata.create_all(bind=engine) 