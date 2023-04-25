import datetime

from sqlalchemy import String, Integer, DateTime, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.consts import Config
from src.db.base_model import BaseModel


class Game(BaseModel):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    orientation = Column(String(1), nullable=False)
    prev_moves = Column(String)
    last_move = Column(String(4))
    check = Column(String(2))
    fen = Column(String(128), default=Config.START_FEN, nullable=False)
    who_win = Column(String(1), default=None)
    created_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    modified_time = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)
    is_active = Column(Boolean,  default=True, nullable=False, index=True)  # index?

    user = relationship("User", back_populates="games")

    def __repr__(self):
        return self._repr(
            id=self.id,
            user_id=self.user_id,
            orientation=self.orientation,
            prev_moves=self.prev_moves,
            last_move=self.last_move,
            check=self.check,
            fen=self.fen,
            who_win=self.who_win,
            created_time=self.created_time,
            modified_time=self.modified_time,
            is_active=self.is_active
        )
