import datetime

from sqlalchemy import String, Integer, DateTime, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.db.base_model import BaseModel


start_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'


class Game(BaseModel):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    orientation = Column(String, nullable=False)
    prev_moves = Column(String)
    last_move = Column(String)
    check = Column(String)
    fen = Column(String, default=start_fen, nullable=False)
    who_win = Column(String, default=None)
    created_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    modified_time = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)
    is_active = Column(Boolean,  default=True, nullable=False)

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
