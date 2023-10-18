from typing import Sequence

from src.database import database
from src.external.weather import WeatherAPI
from src.managers.city import CityManager
from src.models import City
from src.schema.weather import WeatherSchema


async def update_weather():
    async with database.session() as session, session.begin():
        cities: Sequence[City] = await CityManager.get_all(session=session)

        for city in cities:
            weather = await WeatherAPI().get_current_weather_by_city(
                city=city.name,
            )

            data = WeatherSchema(weather=weather)

            await CityManager.update(id_=city.id, data=data, session=session)
