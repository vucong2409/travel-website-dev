from fastapi.params import Depends
from jose.exceptions import JWTError
from sqlalchemy import log
from sqlalchemy.orm.session import Session
import database, models
from typing import final
from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api import login_route, tour_route, login_svc
from fastapi.middleware.cors import CORSMiddleware

# Create all table
models.database.Base.metadata.create_all(bind=database.engine)

list_origins = ['localhost:3000',
                'localhost:5000',
                'falsesight.asia'
                ]

app = FastAPI()
app.include_router(login_route.router)
app.include_router(tour_route.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    # allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

db_ins = next(database.get_db())


@app.get("/", tags=["Default"])
def hello(
    login: models.Login = Depends(login_svc.get_current_user),
):
    return f"Hello {login.login_username}"
