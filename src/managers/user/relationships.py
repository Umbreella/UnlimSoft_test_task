from sqlalchemy.ext.asyncio import AsyncSession

from src.database import BASE
from src.managers.base import BaseManager
from src.managers.picnic import PicnicManager
from src.models import Picnic, User, UserPicnic
from src.schema.user import UserPicnicCreateSchema

from .user import UserManager


class UserPicnicManager(BaseManager):
    model = UserPicnic

    @classmethod
    async def create(
        cls,
        data: UserPicnicCreateSchema,
        session: AsyncSession,
    ) -> BASE:
        user: User | None = await UserManager.get_by_id(
            id_=data.user_id,
            session=session,
        )

        if user is None:
            raise Exception('user not found.')

        picnic: Picnic | None = await PicnicManager.get_by_id(
            id_=data.picnic_id,
            session=session,
        )

        if picnic is None:
            raise Exception('picnic not found.')

        return await super().create(data=data, session=session)
