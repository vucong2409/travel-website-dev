from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime

from sqlalchemy import orm


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login_id: int


class Login_Form(BaseModel):
    login_username: str
    login_password: str


class Login(Login_Form):
    login_id: Optional[int]
    login_role_id: Optional[int]

class User(BaseModel):
    user_id: Optional[int]
    username: str
    nationality: str
    phone: str
    address: str
    city: str
    email: str

class UserRegisterForm(User):
    password: str

class TourOut(BaseModel):
    tour_id: str
    place_id: Optional[str]
    tourguide_id: Optional[str]
    type_id: Optional[str]
    transport: str
    departure_place: str
    adult_price: str
    kid_price: str
    start_date: date
    end_date: date
    seat: int
    tour_desc: Optional[str]

    class Config:
        orm_mode = True

class TourID(BaseModel):
    tour_id: str
