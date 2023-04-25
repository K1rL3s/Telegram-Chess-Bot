import datetime

from sqlalchemy import Integer, DateTime, Column, Boolean, String
from sqlalchemy.orm import relationship

from src.db.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    user_id = Column(Integer, nullable=False, unique=True, index=True)
    name = Column(String(32), nullable=False)
    total_games = Column(Integer, default=0, nullable=False)
    total_wins = Column(Integer, default=0, nullable=False)
    total_defeats = Column(Integer, default=0, nullable=False)
    total_draws = Column(Integer, default=0, nullable=False)
    created_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    modified_time = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    games = relationship('Game', back_populates='user')
    settings = relationship('Settings', back_populates='user')

    def __repr__(self):
        return self._repr(
            id=self.id,
            user_id=self.user_id,
            total_games=self.total_games,
            total_wins=self.total_wins,
            total_defeats=self.total_defeats,
            total_draws=self.total_draws,
            created_time=self.created_time,
            modified_time=self.modified_time,
            is_active=self.is_active,
        )
