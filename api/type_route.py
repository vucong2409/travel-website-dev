from fastapi import FastAPI, Response, routing, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from api import type_svc

import database, schemas, models
from .login_svc import get_current_user

router = APIRouter(prefix='/type', tags=['Type'])

@router.get('/get-all')
def get_all_type(db: Session = Depends(database.get_db)):
    return type_svc.get_all_type(db)

