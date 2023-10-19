from urllib.parse import urlencode

from fastapi import status
from httpx import AsyncClient, Response

from src.models import City, Picnic
from src.schema import CitySchema


class TestPicnicList:
    tested_url = '/api/picnics'

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
        picnic: Picnic,
    ):
        params = urlencode(
            {
                'datetime': picnic.time,
            },
        )

        response: Response = await client.get(f'{self.tested_url}?{params}')

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        [real_picnic] = response.json()

        expected_id = picnic.id
        real_id = real_picnic.get('id')

        assert expected_status == real_status
        assert expected_id == real_id

    async def test_When_GetWithPast_Should_ReturnAllData(
        self,
        client: AsyncClient,
        picnic: Picnic,
        future_picnic: Picnic,
    ):
        params = urlencode(
            {
                'past': False,
            },
        )

        response: Response = await client.get(f'{self.tested_url}?{params}')

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        [real_picnic] = response.json()

        expected_id = future_picnic.id
        real_id = real_picnic.get('id')

        assert expected_status == real_status
        assert expected_id == real_id

    async def test_When_Get_Should_ReturnFutureData(
        self,
        client: AsyncClient,
        picnic: Picnic,
        future_picnic: Picnic,
    ):
        response: Response = await client.get(self.tested_url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        [first_picnic, second_picnic] = response.json()

        assert expected_status == real_status

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
                    'loc': ['body', 'city_id'],
                    'msg': 'Field required',
                    'type': 'missing',
                    'url': 'https://errors.pydantic.dev/2.4/v/missing'
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
        data = {
            'city_id': 1,
            'time': '2023-10-19T08:01:09.478Z',
        }

        response: Response = await client.post(self.tested_url, json=data)

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = {
            'detail': [
                {
                    'city_id': 'Not found.',
                },
            ],
        }
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data

    async def test_When_PostWithValidData_Should_ReturNewInstance(
        self,
        client: AsyncClient,
        city: City,
    ):
        data = {
            'city_id': city.id,
            'time': '2023-10-19T08:01:09.478Z',
        }

        response: Response = await client.post(self.tested_url, json=data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = {
            'id': 1,
            'time': '2023-10-19T08:01:09.478000Z',
            'city': CitySchema.model_validate(city).model_dump(),
            'users': [],
        }
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data
