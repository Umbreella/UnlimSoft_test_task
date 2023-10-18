from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import get_db
from src.managers.picnic import PicnicManager
from src.models import Picnic
from src.schema import PicnicCreateSchema, PicnicSchema, PicnicWithUsersSchema


class PicnicList:
    @classmethod
    async def get_list(
        cls,
        session: AsyncSession = Depends(get_db),
    ) -> list[PicnicWithUsersSchema]:
        data: Sequence[Picnic] = await PicnicManager.get_all(session=session)

        return [
            PicnicWithUsersSchema.model_validate(picnic) for picnic in data
        ]

    @classmethod
    async def create(
        cls,
        data: PicnicCreateSchema,
        session: AsyncSession = Depends(get_db),
    ) -> PicnicSchema:
        new_instance: Picnic = await PicnicManager.create(
            data=data,
            session=session,
        )

        instance: Picnic = (await session.execute(
            select(
                Picnic,
            ).options(
                joinedload(Picnic.city),
            ).where(
                Picnic.id == new_instance.id,
            )
        )).unique().scalar_one()

        return PicnicSchema.model_validate(instance)
