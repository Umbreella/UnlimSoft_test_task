from httpx import AsyncClient, Response
from starlette import status

from src.models import City, Picnic, User
from src.schema import CitySchema, UserPicnicCreateSchema, UserSchema


class TestUserPicnicList:
    tested_url = '/api/picnics/register'

    async def test_When_PostWithEmptyData_Should_ErrorBadRequest(
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
                    'loc': ['body', 'user_id'],
                    'msg': 'Field required',
                    'type': 'missing',
                    'url': 'https://errors.pydantic.dev/2.4/v/missing',
                },
                {
                    'input': {},
                    'loc': ['body', 'picnic_id'],
                    'msg': 'Field required',
                    'type': 'missing',
                    'url': 'https://errors.pydantic.dev/2.4/v/missing',
                },
            ],
        }
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data

    async def test_When_PostWithNotFoundUser_Should_ErrorBadRequest(
        self,
        client: AsyncClient,
    ):
        data = UserPicnicCreateSchema(
            user_id=1,
            picnic_id=1,
        ).model_dump()

        response: Response = await client.post(self.tested_url, json=data)

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = {
            'detail': [
                {
                    'user_id': 'Not found.',
                },
            ],
        }
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data

    async def test_When_PostWithNotPicnicUser_Should_ErrorBadRequest(
        self,
        client: AsyncClient,
        user: User,
    ):
        data = UserPicnicCreateSchema(
            user_id=user.id,
            picnic_id=1,
        ).model_dump()

        response: Response = await client.post(self.tested_url, json=data)

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = {
            'detail': [
                {
                    'picnic_id': 'Not found.',
                },
            ],
        }
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data

    async def test_When_PostWithValidData_Should_ReturnNewInstance(
        self,
        client: AsyncClient,
        user: User,
        picnic: Picnic,
        city: City,
    ):
        data = UserPicnicCreateSchema(
            user_id=user.id,
            picnic_id=picnic.id,
        ).model_dump()

        response: Response = await client.post(self.tested_url, json=data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data = {
            'id': 1,
            'user': UserSchema.model_validate(user).model_dump(),
            'picnic': {
                'id': picnic.id,
                'time': picnic.time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'city': CitySchema.model_validate(city).model_dump(),
            },
        }
        real_data = response.json()

        assert expected_status == real_status
        assert expected_data == real_data
