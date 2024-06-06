from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
from auth import auth_handler

router = APIRouter(
    prefix="/author",
    tags=["author"],
)


@router.get("/", response_model=List[pyd.BaseAuthor])
async def get_authors(db: Session = Depends(get_db)):
    return db.query(models.Author).all()


@router.post("/", response_model=pyd.BaseAuthor)
async def create_author(author: pyd.AuthorName, userid=Depends(auth_handler.auth_wrapper),
                        db: Session = Depends(get_db)):
    author_db = models.Author(name=author.name)
    db.add(author_db)
    db.commit()

    return author_db


@router.put("/{author_id}", response_model=pyd.BaseAuthor)
async def update_author(author_id: int, author: pyd.AuthorName, userid=Depends(auth_handler.auth_wrapper),
                        db: Session = Depends(get_db)):
    author_db = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author_db:
        raise HTTPException(status_code=404, detail='Author not found')

    author_db.name = author.name
    db.add(author_db)
    db.commit()

    return author_db


@router.delete("/{author_id}")
async def delete_author(author_id: int, userid=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    author_db = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author_db:
        raise HTTPException(status_code=404, detail='Author not found')

    db.delete(author_db)
    db.commit()

    return True
