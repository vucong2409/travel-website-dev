from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import schemas, models

router = APIRouter(prefix="/tours", tags=["Tours"])


@router.get("/", response_model=List[schemas.TourOut])
def get_tours(db: Session = Depends(get_db)):
    tours = db.query(models.Tour).all()
    return tours
