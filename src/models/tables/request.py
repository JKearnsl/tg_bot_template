from sqlalchemy import Column, String, Integer, Enum, DateTime, func, Boolean, ForeignKey, event
from sqlalchemy.orm import relationship
from db import Base, IntEnum
from datetime import datetime

from models.request import RequestStatus


class MusicRequest(Base):
    __tablename__ = "requests"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("models.tables.user.User", back_populates="requests")

    music_name = Column(String(255))
    artist_name = Column(String(255))
    # todo: даты

    status = Column(IntEnum(RequestStatus), default=RequestStatus.PENDING)
    verified_at = Column(DateTime(timezone=True), onupdate=func.now())
    create_time = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return '<MusicRequest: {}>'.format(self.id)
