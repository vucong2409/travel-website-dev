from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List, Optional

import database
import schemas, models

from .login_svc import get_current_user
from . import tour_svc

router = APIRouter(prefix="/tours", tags=["Tours"])


@router.get("/", response_model=List[schemas.TourOut])
def get_all_tours(db: Session = Depends(database.get_db)):
    """
    Get all tour, use for testing.
    """
    tours = tour_svc.get_all_tour(db)
    return tours


@router.post("/get-tour", response_model=schemas.TourOut)
def get_tour_by_id(tour_id: schemas.TourID, db: Session = Depends(database.get_db)):
    tour = tour_svc.get_tour_by_id(db, tour_id)
    if not tour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {tour_id.tour_id} cannot found",
        )
    return tour


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TourOut)
def create_tours(
    tour: schemas.TourOut,
    db: Session = Depends(database.get_db),
    login: models.Login = Depends(get_current_user),
):

    return tour_svc.create_new_tour(db, tour)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_tours(
    tour_id: schemas.TourID,
    db: Session = Depends(database.get_db),
    login: models.Login = Depends(get_current_user),
):

    if not tour_svc.delete_tour_by_id(db, tour_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tour with id {tour_id.tour_id} cannot found",
        )

    return {"delete_log": f"tour {tour_id} is deleted"}


@router.put("/", response_model=schemas.TourToChange)
def update_tour(
    tour: schemas.TourToChange,
    id: schemas.TourID,
    db: Session = Depends(database.get_db),
    login: models.Login = Depends(get_current_user),
):
    res = tour_svc.update_tour_by_id(db, tour, id)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tour with id {id.tour_id} cannot found",
        )

    return res
