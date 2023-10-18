from http import HTTPStatus
from typing import Any
from urllib.parse import urlencode

from httpx import AsyncClient, Response


class WeatherAPI:
    def __init__(self):
        self._client = AsyncClient(
            base_url='https://api.openweathermap.org/data/2.5/weather',
        )

    async def get_current_weather_by_city(self, city: str) -> str | None:
        params: dict[str, str] = {
            'units': 'metric',
            'appid': '99ba78ee79a2a24bc507362c5288a81b',
            'q': city,
        }

        response: Response = await self._client.get(f'?{urlencode(params)}')

        if response.status_code != HTTPStatus.OK:
            return None

        data: dict[str, Any] = response.json()

        return str(data.get('main').get('temp'))
