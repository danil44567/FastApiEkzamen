from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    id: int = Field(..., gt=0, example=1)
    username: str = Field(..., example='Автор')

class AuthUser(BaseModel):
    username: str = Field(..., example='Пупа Васин')
    password: str = Field(..., example='123')

