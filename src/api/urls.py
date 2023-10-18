from fastapi import FastAPI, status

from src.api.city import CityList
from src.api.picnic import PicnicList
from src.api.user import UserList
from src.api.user.relationships import UserPicnicList


def add_routers(app: FastAPI) -> None:
    app.add_api_route(
        path='/api/cities',
        endpoint=CityList.get_list,
        response_model=CityList.get_list.__annotations__['return'],
        status_code=status.HTTP_200_OK,
        methods=['get'],
        tags=['City'],
    )
    app.add_api_route(
        path='/api/cities',
        endpoint=CityList.create,
        response_model=CityList.create.__annotations__['return'],
        status_code=status.HTTP_201_CREATED,
        methods=['post'],
        tags=['City'],
    )
    app.add_api_route(
        path='/api/picnics',
        endpoint=PicnicList.get_list,
        response_model=PicnicList.get_list.__annotations__['return'],
        status_code=status.HTTP_200_OK,
        methods=['get'],
        tags=['Picnic'],
    )
    app.add_api_route(
        path='/api/picnics',
        endpoint=PicnicList.create,
        response_model=PicnicList.create.__annotations__['return'],
        status_code=status.HTTP_201_CREATED,
        methods=['post'],
        tags=['Picnic'],
    )
    app.add_api_route(
        path='/api/picnics/register',
        endpoint=UserPicnicList.create,
        response_model=UserPicnicList.create.__annotations__['return'],
        status_code=status.HTTP_201_CREATED,
        methods=['post'],
        tags=['Picnic'],
    )
    app.add_api_route(
        path='/api/users',
        endpoint=UserList.get_list,
        response_model=UserList.get_list.__annotations__['return'],
        status_code=status.HTTP_200_OK,
        methods=['get'],
        tags=['User'],
    )
    app.add_api_route(
        path='/api/users',
        endpoint=UserList.create,
        response_model=UserList.create.__annotations__['return'],
        status_code=status.HTTP_201_CREATED,
        methods=['post'],
        tags=['User'],
    )
