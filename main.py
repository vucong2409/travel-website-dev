from fastapi.params import Depends
from jose.exceptions import JWTError
from sqlalchemy import log
from sqlalchemy.orm.session import Session
import database, models
from typing import final
from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api import image_route, login_route, order_route, route_route, tour_route, login_svc, place_route, type_route
from fastapi.middleware.cors import CORSMiddleware

# Create all table
models.database.Base.metadata.create_all(bind=database.engine)

list_origins = ['http://localhost:3000',
                'http://localhost:5000',
                'http://localhost:5500',
                'http://127.0.0.1:5500',
                'http://falsesight.asia',
                'https://falsesight.asia',
                'https://vitra-travel.web.app',
                'http://vitra-travel.web.app',
                'https://travel-web-dev.web.app/',
                'http://travel-web-dev.web.app/',
                'http://localhost:3001',
                'http://localhost:3002'
                ]

app = FastAPI()
app.include_router(login_route.router)
app.include_router(tour_route.router)
app.include_router(place_route.router)
app.include_router(type_route.router)
app.include_router(order_route.router)
app.include_router(route_route.router)
app.include_router(image_route.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

db_ins = next(database.get_db())


@app.get("/", tags=["Default"])
def hello(
    login: models.Login = Depends(login_svc.get_current_user),
):
    return f"Hello {login.login_username}"
