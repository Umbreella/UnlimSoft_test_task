from pydantic import BaseModel


class WeatherSchema(BaseModel):
    weather: str
