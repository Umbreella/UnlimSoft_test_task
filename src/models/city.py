from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import BASE


class City(BASE):
    """
    Город
    """
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    weather = Column(String, nullable=True)

    picnics = relationship('Picnic', back_populates='city')

    def __repr__(self):
        return f'<City "{self.name}">'
