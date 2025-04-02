from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import Base

# Определение типовых переменных для дженериков
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый класс CRUD с универсальными методами для работы с моделями БД
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Инициализация CRUD объекта с указанием модели SQLAlchemy
        
        Args:
            model: Класс модели SQLAlchemy
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Получить запись по ID
        
        Args:
            db: Сессия БД
            id: ID записи
            
        Returns:
            Объект модели или None, если запись не найдена
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Получить несколько записей с пагинацией
        
        Args:
            db: Сессия БД
            skip: Сколько записей пропустить (для пагинации)
            limit: Максимальное количество записей
            
        Returns:
            Список объектов модели
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Создать новую запись
        
        Args:
            db: Сессия БД
            obj_in: Данные для создания записи (схема Pydantic)
            
        Returns:
            Созданный объект модели
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Обновить существующую запись
        
        Args:
            db: Сессия БД
            db_obj: Существующий объект модели
            obj_in: Данные для обновления (схема Pydantic или словарь)
            
        Returns:
            Обновленный объект модели
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        Удалить запись по ID
        
        Args:
            db: Сессия БД
            id: ID записи
            
        Returns:
            Удаленный объект модели
            
        Raises:
            Exception: Если запись не найдена
        """
        obj = db.query(self.model).filter(self.model.id == id).first()
        db.delete(obj)
        db.commit()
        return obj 