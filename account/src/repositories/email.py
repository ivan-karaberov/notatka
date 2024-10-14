from models.user_emails import UserEmail
from utils.repository import SQLAlchemyRepository


class UserEmailRepository(SQLAlchemyRepository):
    model = UserEmail