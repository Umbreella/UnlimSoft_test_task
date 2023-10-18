from sqlalchemy import Column, ForeignKey, Integer

from src.database import BASE


class UserPicnic(BASE):
    """
    Регистрация пользователя на пикник
    """
    __tablename__ = 'user_picnics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    picnic_id = Column(Integer, ForeignKey('picnics.id'), nullable=False)

    def __repr__(self):
        return f'<UserPicnic {self.id}>'
