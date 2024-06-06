from pydantic import BaseModel, Field
from pyd import BaseAuthor


class GetArticle(BaseModel):
    id: int = Field(..., gt=0, example=1)
    name: str = Field(..., example='Автор')
    text: str = Field(..., example='Куча интересного текста')
    author: BaseAuthor


class AddArticle(BaseModel):
    author_id: int = Field(..., gt=0, example=1)
    name: str = Field(..., min_length=3, max_length=255, example='Крутое название')
    text: str = Field(..., min_length=100, max_length=2000, example='Куча интересного текста')

