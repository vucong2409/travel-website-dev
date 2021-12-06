import datetime
from datetime import timedelta, datetime
from jose import JWTError, jwt
from typing import Optional
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic.types import NonPositiveFloat
from sqlalchemy import log
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false, true
import schemas, models, database
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def register_login(db: Session, login: schemas.Login):
    login.login_password = get_password_hash(login.login_password)
    db_login = models.Login(
        login_username=login.login_username,
        login_password=login.login_password,
        login_role_id=1,
    )
    db.add(db_login)
    db.commit()
    db.refresh(db_login)


def register_user(db: Session, user: schemas.User):
    db_user = models.User(
        user_name = user.username,
        nationality = user.nationality,
        phone = user.phone,
        address = user.address,
        city = user.city,
        email = user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

def alter_user(db: Session, user: schemas.UserAlter, login: models.Login):
    user_in_db = db.query(models.User).filter(models.User.user_name == login.login_username).first()

    if user.login_password != None:
        login.login_password = get_password_hash(user.login_password) 
    
    if user.nationality != None:
        user_in_db.nationality = user.nationality
    
    if user.phone != None:
        user_in_db.phone = user.phone
    
    if user.address != None:
        user_in_db.address = user.address
    
    if user.city != None:
        user_in_db.city = user.city
    
    if user.email != None:
        user_in_db.email = user.email
    

    db.add(login)
    db.commit()
    db.refresh(login)

    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)

def get_login_by_username(db: Session, login_name: str):
    return (
        db.query(models.Login).filter(models.Login.login_username == login_name).first()
    )


def authenticate_user(db: Session, username: str, password: str):
    user = get_login_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.login_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


def verify_access_token(token: str, credential_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        login_id: int = payload.get("login_id")

        if login_id is None:
            raise credential_exceptions

        token_data = schemas.TokenData(login_id=login_id)
    except JWTError:
        raise credential_exceptions

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credential_exception)

    login = (
        db.query(models.Login)
        .filter(models.Login.login_id == token_data.login_id)
        .first()
    )

    return login

def get_profile(username: str, db: Session):
    profile = ( db.query(models.User)
            .filter(models.User.user_name == username)
            .first()
    )
    return profile

def admin_or_not(login: models.Login):
    if login.login_role_id != '1':
        return 'true'
    else: 
        return 'false' 