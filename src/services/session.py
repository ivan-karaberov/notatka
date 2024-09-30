from utils.repository import AbstractRepository
from schemas.auth import SessionSchema
from models.session import Session

class SessionService:
    def __init__(self, session_repo: AbstractRepository) -> None:
        self.session_repo = session_repo()

    async def create_session(self, session_detail: SessionSchema):
        session = Session(
            user_id=session_detail.user_id,
            refresh_token=session_detail.refresh_token,
            expires_at=session_detail.expires_at,
            session_uuid=session_detail.session_uuid
        )
        return await self.session_repo.add_one(session)

    async def deactivate_session(self, session_uuid: str) -> bool:
        session = await self.get_session_by_uuid(session_uuid)
       
        if session is None or session.is_deactivated:
            return False

        await self.session_repo.update(session.id, is_deactivated=True)
        return True


    async def get_session_by_uuid(self, session_uuid: str):
        return await self.session_repo.fetch_one(session_uuid=session_uuid)