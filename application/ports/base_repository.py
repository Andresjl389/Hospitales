from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from uuid import UUID

T = TypeVar("T")

class IBaseRepository(ABC, Generic[T]):
    @abstractmethod
    def create(self, entity: T) -> T: ...
    
    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> Optional[T]: ...
    
    @abstractmethod
    def get_all(self) -> List[T]: ...
    
    @abstractmethod
    def update(self, entity: T) -> T: ...
    
    @abstractmethod
    def delete(self, entity_id: UUID) -> bool: ...
    
    @abstractmethod
    def create_without_commit(self, entity: T) -> T: ...
    