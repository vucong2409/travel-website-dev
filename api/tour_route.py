from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy.orm.session import sessionmaker

import database
import schemas, models

from .login_svc import get_current_user
from . import tour_svc
from api import login_svc

router = APIRouter(prefix="/tours", tags=["Tours"])


@router.get("/get-tours", response_model=List[schemas.TourOut])
def get_tours(db: Session = Depends(database.get_db), limit: int = 10, skip: int = 0):
    tours = tour_svc.get_tours(db, limit, skip)
    return tours

@router.post("/search-by-place")
def search_tour_by_place(query_obj: schemas.Place_Query, db: Session = Depends(database.get_db)):
    return tour_svc.query_tour_by_place(db, query_obj.place_id, query_obj.query)

@router.post('/search-by-type')
def search_by_type(query_obj: schemas.Type_Query, db: Session = Depends(database.get_db)):
    return tour_svc.query_tour_by_type(db, query_obj.type_id, query_obj.query)

@router.get("/tour/get/{tour_id}", response_model=schemas.TourOut)
def get_tour_by_id(tour_id: str, db: Session = Depends(database.get_db)):
    tour = tour_svc.get_tour_by_id(db, tour_id)
    if not tour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tour with id {tour_id} cannot found",
        )
    return tour


@router.post("/create")
def create_tours(
    tour: schemas.TourOut,
    db: Session = Depends(database.get_db),
    login: models.Login = Depends(get_current_user),
):

    if (login.login_role_id == '1'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to create tour'
        )
    return tour_svc.create_new_tour(db, tour)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_tours(
    tour_id: str,
    db: Session = Depends(database.get_db),
    login: models.Login = Depends(get_current_user),
):
    if (login.login_role_id == '1'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to delete tour'
        )
    if not tour_svc.delete_tour_by_id(db, tour_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tour with id {tour_id} cannot found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/update", response_model=schemas.TourToChange)
def update_tour(
    tour: schemas.TourToChange,
    tour_id: str,
    db: Session = Depends(database.get_db),
    login: models.Login = Depends(get_current_user),
):
    res = tour_svc.update_tour_by_id(db, tour, tour_id)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tour with id {tour_id} cannot found",
        )

    return res
