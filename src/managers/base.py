from typing import Sequence, Type

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import BASE


class BaseManager:
    model: Type[BASE]

    @classmethod
    async def get_all(cls, session: AsyncSession) -> Sequence[BASE]:
        query = select(cls.model)

        return (await session.execute(query)).scalars().all()

    @classmethod
    async def get_by_id(cls, id_: int, session: AsyncSession) -> BASE:
        query = select(cls.model).where(cls.model.id == id_)

        return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def create(
        cls,
        data: BaseModel,
        session: AsyncSession,
    ) -> BASE:
        query = insert(cls.model).values(
            **data.model_dump(),
        ).returning(cls.model)

        return (await session.execute(query)).scalar_one()
