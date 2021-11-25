from sqlalchemy.orm import Session
from .. import schemas, models, database
from fastapi import status, HTTPException, Depends


def get_all_tour(db: Session = Depends):
    return db.query(models.Tour).all()
