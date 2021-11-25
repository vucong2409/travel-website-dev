from sqlalchemy.orm import Session
import schemas, models, database
from fastapi import status, HTTPException, Depends


def get_all_tour(db: Session):
    return db.query(models.Tour).all()
