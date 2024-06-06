from pydantic import BaseModel, Field
from pyd import BaseUser, GetArticle


class GetComment(BaseModel):
    id: int = Field(..., gt=0, example=1)
    text: str = Field(..., example='Куча интересного текста')
    user: BaseUser
    article: GetArticle


class EditComment(BaseModel):
    text: str = Field(..., example='Куча интересного текста')


class AddComment(EditComment):
    article_id: int = Field(..., gt=0, example=1)
