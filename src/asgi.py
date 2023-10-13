from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database import database


def create_app(init_db: bool = True) -> FastAPI:
    _app = FastAPI(
        title='UnlimSoft',
        docs_url='/api/docs',
    )

    if init_db:
        database.init_db()

        @asynccontextmanager
        async def lifespan(_app: FastAPI):
            yield
            if database._engine is not None:
                await database.close()

    return _app


application = create_app()

if __name__ == '__main__':
    uvicorn.run(application)
