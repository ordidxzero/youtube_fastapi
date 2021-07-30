from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base, BaseMixin


class Videos(Base, BaseMixin):
    __tablename__ = "videos"
    title = Column(String(100), nullable=False, default="")
    description = Column(String(1000), nullable=True, default="")
    video_url = Column(String(2000), nullable=False, default="")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="videos")
    comments = relationship("Comments")
