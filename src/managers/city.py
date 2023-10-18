from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.external.weather import WeatherAPI
from src.managers.base import BaseManager
from src.models import City
from src.schema.city import CityCreateSchema


class CityManager(BaseManager):
    model = City

    @classmethod
    async def create(
        cls,
        data: CityCreateSchema,
        session: AsyncSession,
    ) -> City:
        city: City | None = (await session.execute(
            select(City).where(City.name == data.name)
        )).scalar_one_or_none()

        if city is not None:
            raise Exception('city name duplicate.')

        weather = await WeatherAPI().get_current_weather_by_city(data.name)

        query = insert(cls.model).values(
            **data.model_dump(),
            weather=weather,
        ).returning(cls.model)

        return (await session.execute(query)).scalar_one()

    @classmethod
    async def update(
        cls,
        id_: int,
        data: BaseModel,
        session: AsyncSession,
    ) -> City:
        query = update(City).values(
            **data.model_dump(),
        ).where(
            City.id == id_,
        ).returning(City)

        return (await session.execute(query)).scalar_one()
