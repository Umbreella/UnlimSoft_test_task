from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.managers.user import UserManager
from src.models import User
from src.schema import UserCreateSchema, UserSchema


class UserList:
    @classmethod
    async def get_list(
        cls,
        session: AsyncSession = Depends(get_db),
    ) -> list[UserSchema]:
        data: Sequence[User] = await UserManager.get_all(session=session)

        return [UserSchema.model_validate(user) for user in data]

    @classmethod
    async def create(
        cls,
        data: UserCreateSchema,
        session: AsyncSession = Depends(get_db),
    ) -> UserSchema:
        instance: User = await UserManager.create(data=data, session=session)

        return UserSchema.model_validate(instance)
