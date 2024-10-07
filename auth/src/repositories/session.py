from models.session import Session
from utils.repository import SQLAlchemyRepository


class SessionRepository(SQLAlchemyRepository):
    model = Session