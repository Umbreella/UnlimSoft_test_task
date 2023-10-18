import copy

import pytest

from src.database import database
from src.managers.city import CityManager
from src.models import City
from src.schema import CityCreateSchema


@pytest.fixture
async def city() -> City:
    instance: City

    async with database.session() as session, session.begin():
        instance = copy.copy(
            await CityManager.create(
                data=CityCreateSchema(
                    name='London',
                ),
                session=session,
            ),
        )

    yield instance
