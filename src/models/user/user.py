from sqlalchemy import Column, Integer, String

from src.database import BASE


class User(BASE):
    """
    Пользователь
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=True)

    def __repr__(self):
        return f'<User {self.surname} {self.name}>'
