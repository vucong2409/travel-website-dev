from fastapi.param_functions import Depends
from jose.exceptions import JWTError
from sqlalchemy import log
from sqlalchemy.orm.session import Session
from . import database, models
from typing import final
from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .api import login_route, login_svc, tour_route

# Create all table
models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(login_route.router)
app.include_router(tour_route.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


db_ins = next(database.get_db())


@app.get("/")
def hello(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = login_svc.decode_token(token)
        user: str = payload.get("sub")
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    login = login_svc.get_login_by_username(db_ins, user)
    if login is None:
        raise credentials_exception
    return "Hello " + user
