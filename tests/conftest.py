import asyncio
from contextlib import ExitStack
from pkgutil import walk_packages

import pytest
from faker import Faker
from httpx import AsyncClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from src.asgi import create_app
from src.config import config
from src.database import database, get_db
from tests import fixtures

module = fixtures
pytest_plugins = [
    *[
        package.name
        for package in walk_packages(
            path=module.__path__,
            prefix=module.__name__ + '.',
        )
    ],
]

faker = Faker(['ru_RU'])
Faker.seed(0)


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield create_app()


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url='http://testserver') as c:
        yield c


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


postgresql_in_docker = factories.postgresql_noproc(
    **{
        'user': config.POSTGRES_USERNAME,
        'password': config.POSTGRES_PASSWORD,
        'host': config.POSTGRES_HOST,
        'port': config.POSTGRES_PORT,
        'dbname': 'test_db',
    }
)


@pytest.fixture(scope='session', autouse=True)
async def connection_test(postgresql_in_docker, event_loop):
    POSTGRES_USER: str = postgresql_in_docker.user
    POSTGRES_PASSWORD = postgresql_in_docker.password
    POSTGRES_HOST = postgresql_in_docker.host
    POSTGRES_PORT = postgresql_in_docker.port
    POSTGRES_DATABASE = postgresql_in_docker.dbname

    with DatabaseJanitor(
        **{
            'user': POSTGRES_USER,
            'host': POSTGRES_HOST,
            'port': POSTGRES_PORT,
            'dbname': POSTGRES_DATABASE,
            'password': POSTGRES_PASSWORD,
            'version': postgresql_in_docker.version,
        }
    ):
        database_url = 'postgresql+asyncpg://%s:%s@%s:%s/%s' % (
            POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT,
            POSTGRES_DATABASE,
        )

        database.init_db(database_url=database_url)
        yield
        await database.close()


@pytest.fixture(scope='function', autouse=True)
async def create_tables(connection_test):
    async with database.connect() as connection:
        await database.drop_all(connection)
        await database.create_all(connection)


@pytest.fixture(scope='function', autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with database.session() as session, session.begin():
            yield session

    app.dependency_overrides[get_db] = get_db_override
