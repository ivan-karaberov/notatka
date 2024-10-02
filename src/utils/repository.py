from abc import ABC, abstractmethod

from sqlalchemy import select, update, func

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
    async def fetch_paginated(self, page: int, page_size: int, **filters):
        raise NotImplementedError

    @abstractmethod
    async def update(id:int, **filters):
        raise NotImplementedError

    @abstractmethod
    async def update_multiply(id: list[int], **filters):
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
    
    async def fetch_paginated(self, page: int, page_size: int, **filters):
        async with db_helper.session_factory() as session:
            total = await session.execute(
                select(func.count(self.model.id)).filter_by(**filters)
            )
            total = total.scalar() or 0
            total_page = (total // page_size) + (1 if total % page_size > 0 else 0)
            offset = (page-1)*page_size
            stmt = (
                select(self.model).
                filter_by(**filters).
                order_by(self.model.created_at.desc()).
                offset(offset).
                limit(page_size)
            )
            res = await session.execute(stmt)
            return total_page, res.scalars().all()

    async def update(self, id: int, **filters):
        async with db_helper.session_factory() as session:
            stmt = (
                update(self.model).
                filter_by(id=id).
                values(**filters)
            )
            await session.execute(stmt)
            await session.commit()

    async def update_multiply(self, id: list[int], **filters):
        async with db_helper.session_factory() as session:
            stmt = (
                update(self.model).
                where(self.model.id.in_(id)).
                values(**filters)
            )
            await session.execute(stmt)
            await session.commit()
