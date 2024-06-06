from sqlalchemy.orm import Session
from database import engine
import models
from auth import auth_handler

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    author = models.Author(name='Вася Пупкин')
    article = models.Article(name='Статья про Танки',
                             text='Советские танки самые крутые, они делают с немецкими хрум-хрум', author=author)
    user = models.User(username='Пупа Васин', password=auth_handler.get_password_hash('123'))
    comment = models.Comment(text='Очень интересная и крутая статья', user=user, article=article)

    session.add_all([author, article, user, comment])
    session.commit()
