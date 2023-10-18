from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import BASE


class User(BASE):
    """
    Пользователь
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    surname: str = Column(String, nullable=False)
    age: str = Column(Integer, nullable=True)

    picnics = relationship(
        'Picnic',
        secondary='user_picnics',
        back_populates='users',
    )

    def __repr__(self):
        return f'<User {self.surname} {self.name}>'
