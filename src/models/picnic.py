from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database import BASE


class Picnic(BASE):
    """
    Пикник
    """
    __tablename__ = 'picnics'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    city_id: int = Column(Integer, ForeignKey('cities.id'), nullable=False)
    time: datetime = Column(DateTime(timezone=True), nullable=False)

    city = relationship('City', back_populates='picnics')
    users = relationship(
        'User',
        secondary='user_picnics',
        back_populates='picnics',
    )

    def __repr__(self):
        return f'<Picnic {self.id}>'
