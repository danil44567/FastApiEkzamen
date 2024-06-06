from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
from auth import auth_handler

router = APIRouter(
    prefix="/article",
    tags=["article"],
)


@router.get("/", response_model=List[pyd.GetArticle])
async def get_articles(db: Session = Depends(get_db)):
    return db.query(models.Article).all()


@router.post("/", response_model=pyd.GetArticle)
async def create_article(article: pyd.AddArticle, userid=Depends(auth_handler.auth_wrapper),
                         db: Session = Depends(get_db)):
    author_db = db.query(models.Author).filter(models.Author.id == article.author_id).first()
    if not author_db:
        raise HTTPException(status_code=404, detail='Author not found')

    article_db = models.Article(name=article.name, text=article.text, author=author_db)
    db.add(article_db)
    db.commit()

    return article_db


@router.put("/{article_id}", response_model=pyd.GetArticle)
async def update_author(article_id: int, article: pyd.AddArticle, userid=Depends(auth_handler.auth_wrapper),
                        db: Session = Depends(get_db)):
    author_db = db.query(models.Author).filter(models.Author.id == article.author_id).first()
    if not author_db:
        raise HTTPException(status_code=404, detail='Author not found')

    article_db = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article_db:
        raise HTTPException(status_code=404, detail='Article not found')

    article_db.name = article.name
    article_db.text = article.text
    article_db.author = author_db

    db.add(article_db)
    db.commit()

    return article_db


@router.delete("/{article_id}")
async def delete_author(article_id: int, userid=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    article_db = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article_db:
        raise HTTPException(status_code=404, detail='Article not found')

    db.delete(article_db)
    db.commit()

    return True
