from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base, BaseMixin


class Comments(Base, BaseMixin):
    __tablename__ = "comments"
    text = Column(String(1000), nullable=False, default="")
    user_id = Column(Integer, ForeignKey("users.id"))
    video_id = Column(Integer, ForeignKey("videos.id"))
    user = relationship("Users")
