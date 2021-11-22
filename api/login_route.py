from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm import Session
from main import database
import schemas
from . import login_svc

router = APIRouter(
    prefix='/login'
)

@router.post('/token', response_model=schemas.Token)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    login = login_svc.authenticate_user(db, form_data.username, form_data.password)
    if not login:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=30)
    access_token = login_svc.create_access_token(
        data={'sub': login.login_username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type' : 'bearer'}

@router.post('/signup')
async def signup(login_info: schemas.Login_Form, db: Session = Depends(database.get_db)):
    login_reg = schemas.Login(login_username=login_info.login_username, login_password=login_info.login_password, login_user_role=1)
    login_svc.register_login(db, login_reg) 
    return "success"
