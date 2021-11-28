from fastapi.applications import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import schemas, models
from fastapi import status, HTTPException, Depends

def get_all_place(db: Session):
    return db.query(models.Place).all()

def get_place_by_id(db: Session, id: str):
    return db.query(models.Place).filter(models.Place.place_id == id).first()

def create_place(db: Session, place: schemas.Place):
    new_place = models.Place(**place.dict())

    db.add(new_place)
    db.commit()
    db.refresh

def delete_place(db: Session, id: str):
    place = db.query(models.Place).filter(models.Place.place_id == id)

    if (place.first() == None):
        return False
    
    place.delete(synchronize_session=False)
    db.commit()

    return True