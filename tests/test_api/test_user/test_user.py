import random

from fastapi import status
from httpx import AsyncClient, Response

from src.models import User
from src.schema import UserCreateSchema, UserSchema
from tests.conftest import faker


class TestUserList:
    tested_url = '/api/users'

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

    async def test_When_GetWithData_Should_ReturnData(
        self,
        client: AsyncClient,
        user: User,
    ):
        response: Response = await client.get(self.tested_url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = [
            UserSchema.model_validate(user).model_dump(),
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
                {
                    'input': {},
                    'loc': ['body', 'surname'],
                    'msg': 'Field required',
                    'type': 'missing',
                    'url': 'https://errors.pydantic.dev/2.4/v/missing',
                },
                {
                    'input': {},
                    'loc': ['body', 'age'],
                    'msg': 'Field required',
                    'type': 'missing',
                    'url': 'https://errors.pydantic.dev/2.4/v/missing',
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
        data = UserCreateSchema(
            name=faker.first_name(),
            surname=faker.last_name(),
            age=random.randint(10, 50),
        ).model_dump()

        response: Response = await client.post(self.tested_url, json=data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = {
            **data,
            'id': 1,
        }
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data
