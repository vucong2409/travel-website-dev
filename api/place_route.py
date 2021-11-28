from fastapi import FastAPI, Response, routing, status, HTTPException, APIRouter
from fastapi.params import  Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from api import place_svc

import database, schemas, models
from .login_svc import get_current_user

router = APIRouter(prefix='/place', tags=["Place"])

@router.get('/get-all')
def get_all_place(db: Session = Depends(database.get_db)):
    return place_svc.get_all_place(db)

@router.get('/get', response_model=schemas.Place)
def get_tour_by_id(id: str, db: Session = Depends(database.get_db)):
    return place_svc.get_place_by_id(db, id)

@router.post('/create')
def create_place(place: schemas.Place ,db: Session = Depends(database.get_db)):
    place_svc.create_place(db, place)
    return "success"

@router.delete('/delete')
def delete_place(id: str, db: Session = Depends(database.get_db)):
    if not place_svc.delete_place(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'tour with id {id} not found'
        )
    return "success"

