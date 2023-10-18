from typing import Sequence

from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.managers.city import CityManager
from src.models import City
from src.schema.city import CityCreateSchema, CitySchema
from src.tasks import update_weather


class CityList:
    @classmethod
    async def get_list(
        cls,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_db),
    ) -> list[CitySchema]:
        background_tasks.add_task(update_weather)

        data: Sequence[City] = await CityManager.get_all(session=session)

        return [CitySchema.model_validate(city) for city in data]

    @classmethod
    async def create(
        cls,
        data: CityCreateSchema,
        session: AsyncSession = Depends(get_db),
    ) -> CitySchema:
        instance: City = await CityManager.create(data=data, session=session)

        return CitySchema.model_validate(instance)
