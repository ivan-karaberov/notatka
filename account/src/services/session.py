from typing import List

from datetime import datetime

from utils.repository import AbstractRepository
from schemas.auth import SessionSchema
from models.session import Session

class SessionService:
    def __init__(self, session_repo: AbstractRepository) -> None:
        self.session_repo = session_repo()

    async def create_session(self, session_detail: SessionSchema):
        """Создает запись о новой сессии"""
        session = Session(
            user_id=session_detail.user_id,
            refresh_token=session_detail.refresh_token,
            expires_at=session_detail.expires_at,
            session_uuid=session_detail.session_uuid
        )
        return await self.session_repo.add_one(session)

    async def deactivate_session(self, session_uuid: str) -> bool:
        """Закрывает сессию"""
        session = await self.get_session_by_uuid(session_uuid)
       
        if session is None or session.is_deactivated:
            return False

        await self.session_repo.update(session.id, is_deactivated=True)
        return True

    async def deactivate_sessions(self, id: list[int]):
        """Закрывает список сессий"""
        await self.session_repo.update_multiply(id, is_deactivated=True)

    async def get_session_by_uuid(self, session_uuid: str):
        """Получаеь uuid сессии"""
        return await self.session_repo.fetch_one(session_uuid=session_uuid)

    async def update_refresh_token(
        self, 
        session_id: int,
        refresh_token: str,
        expires_at: datetime
    ):
        """Обновляет ключ в сессии"""
        await self.session_repo.update(
            id=session_id,
            refresh_token=refresh_token,
            expires_at=expires_at
        )
    
    async def get_all_active_sessions(self, id: int) -> List[SessionSchema]:
        """Получает все активные сессии для заданного пользователя"""
        return await self.session_repo.fetch_all(
            id=id,
            is_deactivated=False,
            expires_at=datetime.now()
        )