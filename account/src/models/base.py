from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, \
                            declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"