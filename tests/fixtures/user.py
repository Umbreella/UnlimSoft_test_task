import copy
import random

import pytest

from src.database import database
from src.managers.user import UserManager
from src.models import User
from src.schema import UserCreateSchema
from tests.conftest import faker


@pytest.fixture
async def user() -> User:
    instance: User

    async with database.session() as session, session.begin():
        instance = copy.copy(
            await UserManager.create(
                data=UserCreateSchema(
                    name=faker.first_name(),
                    surname=faker.last_name(),
                    age=random.randint(10, 50),
                ),
                session=session,
            ),
        )

    yield instance
