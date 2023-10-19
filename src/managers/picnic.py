from datetime import datetime
from typing import Sequence, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import BASE
from src.managers.base import BaseManager
from src.managers.city import CityManager
from src.models import City, Picnic
from src.schema.picnic import PicnicCreateSchema


class PicnicManager(BaseManager):
    model = Picnic

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        time: datetime | None = None,
        past: bool | None = False,
    ) -> Sequence[Type[BASE]]:
        query = select(
            Picnic,
        ).options(
            joinedload(Picnic.city),
            joinedload(Picnic.users),
        )

        if time:
            query = query.where(Picnic.time == time)

        if not past:
            query = query.where(Picnic.time >= datetime.now())

        return (await session.execute(query)).unique().scalars().all()

    @classmethod
    async def create(
        cls,
        data: PicnicCreateSchema,
        session: AsyncSession,
    ) -> Type[BASE]:
        city: City | None = await CityManager.get_by_id(
            id_=data.city_id,
            session=session,
        )

        if city is None:
            raise Exception(
                {
                    'city_id': 'Not found.',
                },
            )

        return await super().create(data=data, session=session)
