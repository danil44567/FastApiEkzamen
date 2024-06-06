from pydantic import BaseModel, Field


class BaseAuthor(BaseModel):
    id: int = Field(..., gt=0, example=1)
    name: str = Field(..., max_length=255, example='Автор')


class AuthorName(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, example='Автор')
