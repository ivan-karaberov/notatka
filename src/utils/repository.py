from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update

from core.db.db_helper import db_helper


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(data: dict):
        raise NotImplementedError

    @abstractmethod
    async def fetch_one(**filters):
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(**filters):
        raise NotImplementedError

    @abstractmethod
    async def update(id:int, **filters):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, model) -> bool:
        async with db_helper.session_factory() as session:
            session.add(model)
            await session.commit()
            return True

    async def fetch_one(self, **filters):
        async with db_helper.session_factory() as session:
            stmt = select(self.model).filter_by(**filters).limit(1)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def fetch_all(self, **filters):
        async with db_helper.session_factory() as session:
            stmt = select(self.model)
            for key, value in filters.items():
                if isinstance(value, list):
                    stmt = stmt.filter(getattr(self.model, key).in_(value))
                else:
                    stmt = stmt.filter(getattr(self.model, key) == value)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def update(self, id: int, **filters):
        async with db_helper.session_factory() as session:
            stmt = (
                update(self.model).
                filter_by(id=id).
                values(**filters)
            )
            await session.execute(stmt)
            await session.commit()