from typing import TypeVar, Generic, Type, Optional, List
from sqlmodel import select, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations"""

    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    def get_by_id(self, id: str) -> Optional[T]:
        """Get entity by ID"""
        return self.session.get(self.model, id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination"""
        statement = select(self.model).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def create(self, entity: T) -> T:
        """Create new entity"""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        """Update existing entity"""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, id: str) -> bool:
        """Delete entity by ID"""
        entity = self.get_by_id(id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False
