from sqlalchemy.orm import Session, query
import schemas, models
from fastapi import status, HTTPException, Depends

INVALID_COMMENT_ID = 1
UNAUTHORIZED = 2

def get_comments_by_tour_id(db: Session, tour_id: str):
    return db.query(models.Comment).filter(models.Comment.tour_id == tour_id).all()


def get_user(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        return False
    return user

def get_user_id_by_username(db: Session, username: str):
    return (db.query(models.User).filter(models.User.user_name == username).first().user_id)

def create_new_comment(db: Session, comment: schemas.CommentPost, username: str):
    
    current_user_id = get_user_id_by_username(db, username)

    new_comment = models.Comment(user_id=current_user_id, **comment.dict())

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment

def delete_comment(db: Session, comment_id: int, username: str):
    comment_query = db.query(models.Comment).filter(models.Comment.comment_id == comment_id)

    comment = comment_query.first()
    
    if comment == None:
        return INVALID_COMMENT_ID
    
    if comment.user_id != get_user_id_by_username(db, username):
        return UNAUTHORIZED

    comment_query.delete(synchronize_session=False)
    db.commit()

def update_comment(db: Session, comment_id: int, username: str, updated_comment: schemas.CommentUpdate):
    comment_query = db.query(models.Comment).filter(models.Comment.comment_id == comment_id)

    comment = comment_query.first()

    if comment == None:
        return INVALID_COMMENT_ID
    
    if comment.user_id != get_user_id_by_username(db, username):
        return UNAUTHORIZED

    comment_query.update(updated_comment.dict(), synchronize_session=False)
    db.commit()

    return comment_query.first()