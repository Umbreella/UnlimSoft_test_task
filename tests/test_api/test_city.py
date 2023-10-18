from urllib.parse import urlencode

from fastapi import status
from httpx import AsyncClient, Response

from src.models import City
from src.schema import CityCreateSchema, CitySchema


class TestCityList:
    tested_url = '/api/cities'

    async def test_When_GetWithEmptyData_Should_ReturnEmptyData(
        self,
        client: AsyncClient,
    ):
        response: Response = await client.get(self.tested_url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = []
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data

    async def test_When_GetWithFilter_Should_ReturnFilterData(
        self,
        client: AsyncClient,
        city: City,
    ):
        params = urlencode(
            {
                'q': 'randomsearch',
            },
        )

        response: Response = await client.get(f'{self.tested_url}?{params}')

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = []
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data

    async def test_When_GetWithData_Should_ReturnData(
        self,
        client: AsyncClient,
        city: City,
    ):
        response: Response = await client.get(self.tested_url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = [
            CitySchema.model_validate(city).model_dump(),
        ]
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data

    async def test_When_PostWithNotValidData_Should_ErrorBadRequest(
        self,
        client: AsyncClient,
    ):
        response: Response = await client.post(self.tested_url, json={})

        expected_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        real_status = response.status_code

        expected_data = {
            'detail': [
                {
                    'input': {},
                    'loc': ['body', 'name'],
                    'msg': 'Field required',
                    'type': 'missing',
                    'url': 'https://errors.pydantic.dev/2.4/v/missing',
                },
            ],
        }
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data

    async def test_When_PostWithDuplicateData_Should_ErrorBadRequest(
        self,
        client: AsyncClient,
        city: City,
    ):
        data = CityCreateSchema(
            name=city.name,
        ).model_dump()

        response: Response = await client.post(self.tested_url, json=data)

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = {
            'detail': [
                {
                    'name': 'This value is exists.',
                },
            ],
        }
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data

    async def test_When_PostWithNotValidName_Should_ErrorBadRequest(
        self,
        client: AsyncClient,
    ):
        data = CityCreateSchema(
            name='RandomText',
        ).model_dump()

        response: Response = await client.post(self.tested_url, json=data)

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = {
            'detail': [
                {
                    'name': 'This value is not City.',
                },
            ],
        }
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data

    async def test_When_PostWithValidData_Should_ReturNewInstance(
        self,
        client: AsyncClient,
    ):
        data = CityCreateSchema(
            name='London',
        ).model_dump()

        response: Response = await client.post(self.tested_url, json=data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = {
            **data,
            'id': 1,
        }
        real_data = response.json()

        expected_weather = None
        real_weather = real_data.pop('weather')

        assert expected_status == real_status
        assert expected_data == real_data
        assert expected_weather != real_weather
