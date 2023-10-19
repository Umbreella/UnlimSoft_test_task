import copy
from datetime import datetime, timedelta

import pytest

from src.database import database
from src.managers.picnic import PicnicManager
from src.models import City, Picnic
from src.schema import PicnicCreateSchema


@pytest.fixture
async def picnic(city: City) -> Picnic:
    instance: Picnic

    async with database.session() as session, session.begin():
        instance = copy.copy(
            await PicnicManager.create(
                data=PicnicCreateSchema(
                    city_id=city.id,
                ),
                session=session,
            ),
        )

    yield instance


@pytest.fixture
async def future_picnic(city: City) -> Picnic:
    instance: Picnic

    async with database.session() as session, session.begin():
        instance = copy.copy(
            await PicnicManager.create(
                data=PicnicCreateSchema(
                    city_id=city.id,
                    time=datetime.now() + timedelta(days=2),
                ),
                session=session,
            ),
        )

    yield instance
