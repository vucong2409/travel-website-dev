from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic.errors import PathNotADirectoryError
from sqlalchemy import schema
from sqlalchemy.ext import declarative
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.functions import mode
import database, schemas
from . import login_svc
import models

router = APIRouter(prefix="/login", tags=["Login"])


@router.post("/token", response_model=schemas.Token)
async def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user_login = login_svc.authenticate_user(db, form_data.username, form_data.password)
    if not user_login:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = login_svc.create_access_token(
        data={"login_id": user_login.login_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token-json", response_model=schemas.Token)
async def get_access_token(
    form: schemas.Login_Form,
    db: Session = Depends(database.get_db),
):
    user_login = login_svc.authenticate_user(db, form.login_username, form.login_password)
    if not user_login:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = login_svc.create_access_token(
        data={"login_id": user_login.login_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/signup")
async def signup(
    login_info: schemas.UserRegisterForm, db: Session = Depends(database.get_db)
):
    user_reg = schemas.User(
        username = login_info.username,
        nationality = login_info.nationality,
        phone = login_info.phone,
        address = login_info.address,
        city = login_info.city,
        email = login_info.email
    )
    login_svc.register_user(db, user_reg)

    login_reg = schemas.Login(
        login_username=login_info.username,
        login_password=login_info.password,
        login_role_id=1,
    )
    login_svc.register_login(db, login_reg)

    return "success"

@router.get("/profile")
async def get_profile(
    login: models.Login = Depends(login_svc.get_current_user), db: Session = Depends(database.get_db)
):
    profile = login_svc.get_profile(login.login_username, db)
    return profile

@router.post("/edit")
async def edit_profile(
    user_alter: schemas.UserAlter,
    login: models.Login = Depends(login_svc.get_current_user),
    db: Session = Depends(database.get_db),
):
    login_svc.alter_user(db, user_alter, login)
    return "success"

@router.get("/isAdmin")
async def check_if_admin_or_not(login: models.Login = Depends(login_svc.get_current_user)):
    return login_svc.admin_or_not(login)