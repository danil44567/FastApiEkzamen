from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
from auth import auth_handler

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


@router.get("/", response_model=List[pyd.GetComment])
async def get_comments(db: Session = Depends(get_db)):
    return db.query(models.Comment).all()


@router.post("/", response_model=pyd.GetComment)
async def create_comment(comment: pyd.AddComment, userid=Depends(auth_handler.auth_wrapper),
                         db: Session = Depends(get_db)):
    user_db = db.query(models.User).filter(models.User.id == userid).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    article_db = db.query(models.Article).filter(models.Article.id == comment.article_id).first()
    if not article_db:
        raise HTTPException(status_code=404, detail='Article not found')

    comment_db = models.Comment(text=comment.text, user=user_db, article=article_db)
    db.add(comment_db)
    db.commit()

    return comment_db


@router.put("/{comment_id}", response_model=pyd.GetComment)
async def update_comment(comment_id: int, comment: pyd.EditComment, userid=Depends(auth_handler.auth_wrapper),
                         db: Session = Depends(get_db)):
    comment_db = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment_db:
        raise HTTPException(status_code=404, detail='Comment not found')

    if comment_db.user_id != userid:
        raise HTTPException(status_code=404, detail='Not your comment')

    comment_db.text = comment.text
    db.add(comment_db)
    db.commit()

    return comment_db


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, userid=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    comment_db = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment_db:
        raise HTTPException(status_code=404, detail='Comment not found')

    if comment_db.user_id != userid:
        raise HTTPException(status_code=404, detail='Not your comment')

    db.delete(comment_db)
    db.commit()

    return True
