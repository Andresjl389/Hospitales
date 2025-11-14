from uuid import UUID
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, List, Optional

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_id(self, entity_id: UUID) -> T:
        return self.db.query(self.model).filter(self.model.id == entity_id).first()

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()
    
    def update(self, entity: T) -> T:
        self.db.merge(entity)
        self.db.commit()
        return entity

    def delete(self, entity_id: UUID) -> bool:
        entity = self.get_by_id(entity_id)
        if entity:
            self.db.delete(entity)
            self.db.commit()
            return True
        return False