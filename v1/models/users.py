from sqlalchemy import Column, Enum, String, Boolean
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from core.db import Base, BaseMixin


class Users(Base, BaseMixin):
    __tablename__ = "users"
    status = Column(Enum("active", "deleted", "blocked"), default="active")
    email = Column(String(200), nullable=False, default="")
    hashed_password = Column(String(255), default="")
    name = Column(String(100), nullable=True, default="")
    birthdate = Column(String(15), nullable=True, default="")
    gender = Column(TINYINT(2), nullable=True, default=0)
    bio = Column(String(2000), nullable=True, default="")
    profile_image = Column(String(1000), nullable=True, default="")
    verified = Column(Boolean, nullable=True, default=False)
    videos = relationship("Videos", back_populates="user")
