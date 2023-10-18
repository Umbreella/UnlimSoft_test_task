from src.managers.base import BaseManager
from src.models import User


class UserManager(BaseManager):
    model = User
