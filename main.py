import database
from typing import final
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api import user_route


app = FastAPI()
app.include_router(user_route.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/token')

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def hello():
    return {"message" : "Hello"}
