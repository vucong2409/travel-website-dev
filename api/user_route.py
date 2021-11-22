from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from main import database
from schemas import Token

router = APIRouter(
    prefix='/user'
)

@router.post('/token', response_model=Token)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    return {'access_token': 'a', 'token_type': 'bearer'}