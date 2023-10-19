from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.schema.city import CitySchema


class PicnicCreateSchema(BaseModel):
    city_id: int
    time: datetime = datetime.now()


class PicnicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    time: datetime | None
    city: CitySchema
