from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List, Optional, Sequence

import database
import schemas, models

from .login_svc import get_current_user
from . import comment_svc

router = APIRouter(prefix="/comments", tags=["Comment"])


@router.get("/get-comments/{tour_id}", response_model=List[schemas.Comment])
def get_comments_by_tour(tour_id: str, db: Session = Depends(database.get_db)):
    comments = comment_svc.get_comments_by_tour_id(db, tour_id)
                        
    for comment in comments:
        user = comment_svc.get_user(comment.user_id, db)
        comment.user = user
    return comments


@router.post("/create-comments", response_model=schemas.CommentPost)
def create_comment(comment: schemas.CommentPost, db: Session = Depends(database.get_db),
    login: models.Login = Depends(get_current_user)):

    return comment_svc.create_new_comment(db, comment, login.login_username)
    
@router.delete("/detele-comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int, 
    db: Session = Depends(database.get_db), 
    login: models.Login = Depends(get_current_user)
):
    delete_comment_code = comment_svc.delete_comment(db, comment_id, login.login_username)

    if delete_comment_code == comment_svc.INVALID_COMMENT_ID:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {comment_id} does not exist")
                        
    if delete_comment_code == comment_svc.UNAUTHORIZED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("update-comment/{comment_id}", response_model=schemas.CommentUpdate)
def update_comment(
    comment_id: int,
    updated_comment: schemas.CommentUpdate,
    db: Session = Depends(database.get_db),
    login: models.Login = Depends(get_current_user)
):
    new_comment = comment_svc.update_comment(db, comment_id, login.login_username, updated_comment)

    if new_comment == comment_svc.INVALID_COMMENT_ID:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {comment_id} does not exist")
                        
    if new_comment == comment_svc.UNAUTHORIZED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return new_comment