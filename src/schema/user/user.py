from pydantic import BaseModel, ConfigDict


class UserCreateSchema(BaseModel):
    name: str
    surname: str
    age: int


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    surname: str
    age: int
