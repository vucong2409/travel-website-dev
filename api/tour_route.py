from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import schemas, models

from .login_svc import get_current_user
from . import tour_svc

router = APIRouter(prefix="/tours", tags=["Tours"])


@router.get("/", response_model=List[schemas.TourOut])
def get_all_tours(db: Session = Depends(get_db)):
    """
    Get all tour, use for testing.
    """
    tours = tour_svc.get_all_tour()
    return tours


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TourOut)
def create_tours(
    tour: schemas.TourOut,
    db: Session = Depends(get_db),
    login: models.Login = Depends(get_current_user),
):
    new_tour = models.Tour(**tour.dict())

    db.add(new_tour)
    db.commit()
    db.refresh(new_tour)

    return new_tour
