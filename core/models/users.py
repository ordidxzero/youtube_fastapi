from datetime import datetime
from sqlalchemy import Column, Integer, Enum, String, DateTime, func
from sqlalchemy.dialects.mysql import TINYINT
from core.db import Base, BaseMixin


class Users(Base, BaseMixin):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    status = Column(Enum("active", "deleted", "blocked"), default="active")
    email = Column(String(200), nullable=False, default="")
    hashed_password = Column(String(255), default="")
    name = Column(String(100), nullable=True, default="")
    birthdate = Column(String(15), nullable=True, default="")
    gender = Column(TINYINT(2), nullable=True, default=0)
    profile_image = Column(String(1000), nullable=True, default="")
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.utc_timestamp(),
        on_update=func.utc_timestamp(),
    )
