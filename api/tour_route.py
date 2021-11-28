from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List, Optional

import database
import schemas, models

from .login_svc import get_current_user
from . import tour_svc

router = APIRouter(prefix="/tours", tags=["Tours"])


@router.get("/get-tours", response_model=List[schemas.TourOut])
def get_tours(db: Session = Depends(database.get_db), limit: int = 10, skip: int = 0):
    tours = tour_svc.get_tours(db, limit, skip)
    return tours


@router.get("/tour/get/{tour_id}", response_model=schemas.TourOut)
def get_tour_by_id(tour_id: str, db: Session = Depends(database.get_db)):
    tour = tour_svc.get_tour_by_id(db, tour_id)
    if not tour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tour with id {tour_id} cannot found",
        )
    return tour


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=schemas.TourOut
)
def create_tours(
    tour: schemas.TourOut,
    db: Session = Depends(database.get_db),
    login: models.Login = Depends(get_current_user),
):

    return tour_svc.create_new_tour(db, tour)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_tours(
    tour_id: str,
    db: Session = Depends(database.get_db),
    login: models.Login = Depends(get_current_user),
):

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
