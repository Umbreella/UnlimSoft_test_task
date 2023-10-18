from pydantic import BaseModel, ConfigDict

from src.schema.weather import WeatherSchema


class CityCreateSchema(BaseModel):
    name: str


class CitySchema(WeatherSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
