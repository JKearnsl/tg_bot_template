from sqlalchemy import Column, String, Integer, Enum, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from db import Base, IntEnum

from models.role import UserRole
from models.user import UserStatus


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    record_book_id = Column(Integer, unique=True, nullable=True)  # todo: nullable=False?
    role = Column(Enum(UserRole), default=UserRole.USER)
    status = Column(IntEnum(UserStatus), default=UserStatus.UNCONFIRMED)

    requests = relationship("models.tables.request.MusicRequest", back_populates="owner")

    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return '<User: {}>'.format(self.id)
