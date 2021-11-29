from sqlalchemy.orm import Session
import schemas, models
from fastapi import status, HTTPException, Depends

def get_all_type(db: Session):
    return db.query(models.Type).all()

def get_type_by_id(db: Session, id: str):
    return db.query(models.Type).filter(models.Type.type_id == id).first()