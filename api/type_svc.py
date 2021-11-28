from sqlalchemy.orm import Session
import schemas, models
from fastapi import status, HTTPException, Depends

def get_all_type(db: Session):
    return db.query(models.Type).all()