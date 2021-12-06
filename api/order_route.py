from fastapi import FastAPI, Response, routing, status, HTTPException, APIRouter
from fastapi import params
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.functions import mode
from api import order_svc

import database, schemas, models
from .login_svc import get_current_user
from api import login_svc

router = APIRouter(prefix="/order", tags=["Order"])

@router.get("/get-your-order")
def get_all_your_order(login: models.Login = Depends(login_svc.get_current_user), db: Session = Depends(database.get_db)):
    return order_svc.get_your_order(login, db)

@router.get("/get")
def get_order_by_id(id: int, login: models.Login = Depends(login_svc.get_current_user), db: Session = Depends(database.get_db)):
    return order_svc.get_order_by_id(login, db, id)

@router.post("/create")
def create_order(order_form: schemas.OrderForm, login: models.Login = Depends(login_svc.get_current_user), db: Session = Depends(database.get_db)):
    return order_svc.create_your_order(login, order_form, db)

@router.delete('/delete')
def delete_order(id: int, login: models.Login = Depends(login_svc.get_current_user), db = Depends(database.get_db)):
    if not order_svc.delete_order(login, db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'order with id {id} not found'
        )
    return 'success'

@router.get('/get-all-your-unconfirmed-order')
def get_all_your_unconfirmed_order(login: models.Login = Depends(login_svc.get_current_user), db: Session = Depends(database.get_db)):
    return order_svc.get_your_unconfirmed_order(login, db)

@router.get('/get-all-unconfirmed-order-admin')
def get_all_uncomfirmed_order(login: models.Login = Depends(login_svc.get_current_user), db: Session = Depends(database.get_db)):
    result = order_svc.get_all_unconfirmed_order(login, db) 
    if (result == False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not authorized to call this api'
        )
    else:
        return result
    
@router.get('/confirm-order')
def confirm_order(order_id: int, login: models.Login = Depends(login_svc.get_current_user), db: Session = Depends(database.get_db)):
    if not order_svc.confirm_order(login, db, order_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Error'
        )
    else: 
        return 'success'