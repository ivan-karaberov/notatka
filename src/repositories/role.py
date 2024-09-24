from models.role import Role
from utils.repository import SQLAlchemyRepository


class RoleRepository(SQLAlchemyRepository):
    model = Role