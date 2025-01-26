import logging
from abc import ABC, abstractmethod

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.note import *

log = logging.getLogger(__name__)


class AbstractRepository[T](ABC):
    @abstractmethod
    async def add_one(self, obj: T) -> int | None:
        raise NotImplementedError
    
    @abstractmethod
    async def fetch_one(self, **filters) -> T | None:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, id: int, **filters) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> bool:
        raise NotImplementedError


class SQLAlchemyRepository[T](AbstractRepository):
    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session = session
        self.model = model
    
    async def add_one(self, obj: T) -> int | None:
        try:
            self.session.add(obj)
            await self.session.commit()
            return obj.id
        except Exception as e:
            await self.session.rollback()
            log.error("DB Repository failed add_one > %s", e)

    async def fetch_one(self, **filters) -> T | None:
        try:
            query = select(self.model).filter_by(**filters).limit(1)
            user = await self.session.execute(query)
        except Exception as e:
            await self.session.rollback()
            log.error("DB Repository failed fetch_one > %s", e)
            
        return user.scalar_one_or_none()
    
    async def update(self, id: int, **filters) -> T | None:
        try:
            stmt = (
                update(self.model).
                filter_by(id=id).
                values(**filters).
                returning(self.model)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.fetchone()
        except Exception as e:
            await self.session.rollback()
            log.error("DB Repository failed update > %s", e)

    async def delete(self, obj: T) -> bool:
        try:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            log.error("DB Repository failed delete > %s", e)
        return False
