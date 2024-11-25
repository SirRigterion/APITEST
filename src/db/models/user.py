from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base_class import Base

# Модель SQLAlchemy
class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    name: Mapped[str] = mapped_column(String(length=320), nullable=False)
