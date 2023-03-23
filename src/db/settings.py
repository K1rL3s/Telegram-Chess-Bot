import datetime

from sqlalchemy import Integer, DateTime, Column, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel
from ..chess_api.get_limits import get_defaults


class Settings(BaseModel):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    min_time = Column(Integer, nullable=False)
    max_time = Column(Integer, nullable=False)
    threads = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False)
    ram_hash = Column(Integer, nullable=False)
    skill_level = Column(Integer, nullable=False)
    elo = Column(Integer, nullable=False)
    colors = Column(String)  # ?
    with_coords = Column(Boolean, default=True, nullable=False)
    with_position_evaluation = Column(Boolean, default=False, nullable=True)
    size = Column(Integer, nullable=False)
    modified_time = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)

    user = relationship('User', back_populates='settings')

    def __init__(self, **kwargs):
        defaults = get_defaults()
        defaults.update(kwargs)
        super(Settings, self).__init__(**defaults)

    def __repr__(self):
        return self._repr(
            id=self.id,
            user_id=self.user_id,
            min_time=self.min_time,
            max_time=self.max_time,
            threads=self.threads,
            depth=self.depth,
            ram_hash=self.ram_hash,
            skill_level=self.skill_level,
            elo=self.elo,
            colors=self.colors,
            with_coords=self.with_coords,
            with_position_evaluation=self.with_position_evaluation,
            size=self.size,
            modified_time=self.modified_time
        )
