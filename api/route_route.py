from fastapi import FastAPI, Response, routing, status, HTTPException, APIRouter
from fastapi import params
from fastapi.params import Depends
from sqlalchemy.orm import Session
from api import route_svc

import database, schemas, models

router = APIRouter(prefix='/routes', tags=['Route'])

@router.get('/get-by-tour-id')
def get_route_by_tour_id(tour_id: str, db: Session = Depends(database.get_db)):
    return route_svc.get_route_by_tour_id(db, tour_id)

@router.get('/get-by-id')
def get_route_by_id(id: int, db: Session = Depends(database.get_db)):
    return route_svc.get_route_by_route_id(db, id)

@router.post('/create')
def create_route(route: schemas.Routes, db: Session = Depends(database.get_db)):
    route_svc.create_route(db, route)
    return "success"

@router.delete('/delete')
def delete_route_by_id(id: int, db: Session = Depends(database.get_db)):
    if not route_svc.delete_route_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"route with id {id} not found"
        )
    return 'success'

@router.delete('/delete-by-tour-id')
def delete_route_by_tour_id(id: str, db: Session = Depends(database.get_db)):
    if not route_svc.delete_route_by_tour_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Delete failed'
        )
    return 'success'