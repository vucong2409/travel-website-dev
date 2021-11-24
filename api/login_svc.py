import datetime
from datetime import timedelta, datetime
from jose import JWTError, jwt
from typing import Optional
from sqlalchemy import log
from sqlalchemy.orm import Session
import schemas, models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY =  "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def register_login(db: Session, login: schemas.Login):
    login.login_password = get_password_hash(login.login_password)
    db_login = models.Login(login_username=login.login_username, login_password=login.login_password, login_role_id=1)
    db.add(db_login)
    db.commit()
    db.refresh(db_login)

def get_login_by_username(db: Session, login_name: str):
    return db.query(models.Login).filter(models.Login.login_username == login_name).first()

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
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload