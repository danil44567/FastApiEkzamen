from fastapi import FastAPI
from routers import author_router, article_router, comments_router, user_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(author_router.router)
app.include_router(article_router.router)
app.include_router(comments_router.router)
