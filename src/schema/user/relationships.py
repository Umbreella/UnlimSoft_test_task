from pydantic import BaseModel, ConfigDict

from src.schema import PicnicSchema

from .user import UserSchema


class UserPicnicCreateSchema(BaseModel):
    user_id: int
    picnic_id: int


class UserPicnicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: UserSchema
    picnic: PicnicSchema


class PicnicWithUsersSchema(PicnicSchema):
    users: list[UserSchema]
