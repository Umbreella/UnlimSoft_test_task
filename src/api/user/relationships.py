from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import get_db
from src.managers.user import UserPicnicManager
from src.models import UserPicnic
from src.schema import UserPicnicCreateSchema, UserPicnicSchema


class UserPicnicList:
    @classmethod
    async def create(
        cls,
        data: UserPicnicCreateSchema,
        session: AsyncSession = Depends(get_db),
    ) -> UserPicnicSchema:
        new_instance: UserPicnic = await UserPicnicManager.create(
            data=data,
            session=session,
        )

        instance: UserPicnic = (await session.execute(
            select(
                UserPicnic,
            ).options(
                joinedload(UserPicnic.user),
                joinedload(UserPicnic.picnic),
            ).where(
                UserPicnic.id == new_instance.id,
            )
        )).unique().scalar_one()

        return UserPicnicSchema.model_validate(instance)
