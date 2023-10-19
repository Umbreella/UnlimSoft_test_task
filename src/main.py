# import datetime as dt
#
# from fastapi import FastAPI, HTTPException, Query
#
# from database import (
#     Base,
#     City,
#     Picnic,
#     PicnicRegistration,
#     Session,
#     User,
#     engine,
# )
# from external_requests import CheckCityExisting, GetWeatherRequest
# from models import RegisterUserRequest, UserModel
#
# app = FastAPI()
#
#
# @app.get('/picnic-register/', summary='Picnic Registration', tags=['picnic'])
# def register_to_picnic(*_, **__,):
#     """
#     Регистрация пользователя на пикник
#     (Этот эндпойнт необходимо реализовать в процессе выполнения тестового задания)
#     """
#     # TODO: Сделать логику
#     return ...
#
