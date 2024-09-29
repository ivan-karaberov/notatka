from utils.repository import AbstractRepository
from schemas.auth import SessionSchema
from models.session import Session

class SessionService:
    def __init__(self, session_repo: AbstractRepository) -> None:
        self.session_repo = session_repo()

    async def create_session(self, session_detail: SessionSchema) -> bool:
        session = Session(
            user_id=session_detail.user_id,
            refresh_token=session_detail.refresh_token,
            expires_at=session_detail.expires_at
        )
        return await self.session_repo.add_one(session)