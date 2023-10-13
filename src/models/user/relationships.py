from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database import BASE


class UserPicnic(BASE):
    """
    Регистрация пользователя на пикник
    """
    __tablename__ = 'user_picnics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    picnic_id = Column(Integer, ForeignKey('picnics.id'), nullable=False)

    user = relationship('User', backref='picnics')
    picnic = relationship('Picnic', backref='users')

    def __repr__(self):
        return f'<UserPicnic {self.id}>'
