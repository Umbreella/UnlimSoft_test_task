from sqlalchemy import Column, DateTime, ForeignKey, Integer

from src.database import BASE


class Picnic(BASE):
    """
    Пикник
    """
    __tablename__ = 'picnics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    time = Column(DateTime, nullable=False)

    def __repr__(self):
        return f'<Picnic {self.id}>'
