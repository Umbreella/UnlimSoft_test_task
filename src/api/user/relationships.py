from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import get_db
from src.exceptions.bad_request import BadRequest
from src.managers.user import UserPicnicManager
from src.models import Picnic, UserPicnic
from src.schema import UserPicnicCreateSchema, UserPicnicSchema


class UserPicnicList:
    @classmethod
    async def create(
        cls,
        data: UserPicnicCreateSchema,
        session: AsyncSession = Depends(get_db),
    ) -> UserPicnicSchema:
        try:
            new_instance: UserPicnic = await UserPicnicManager.create(
                data=data,
                session=session,
            )
        except Exception as ex:
            raise BadRequest(ex.args)

        instance: UserPicnic = (await session.execute(
            select(
                UserPicnic,
            ).options(
                joinedload(UserPicnic.user),
                joinedload(UserPicnic.picnic).options(joinedload(Picnic.city)),
            ).where(
                UserPicnic.id == new_instance.id,
            )
        )).unique().scalar_one()

        return UserPicnicSchema.model_validate(instance)
