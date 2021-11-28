from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime

from sqlalchemy import orm

from models import City


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
    place_id: Optional[str] = 1
    tourguide_id: Optional[str] = 1
    type_id: Optional[str] = 1
    transport: str
    departure_place: str = "Hà Nội"
    adult_price: str = "1,000,000"
    kid_price: str = "1,000,000"
    start_date: date
    end_date: date
    seat: int
    tour_desc: Optional[str]

    class Config:
        orm_mode = True


class TourToChange(BaseModel):
    place_id: Optional[str] = 1
    tourguide_id: Optional[str] = 1
    type_id: Optional[str] = 1
    transport: str
    departure_place: str = "Hà Nội"
    adult_price: str = "1,000,000"
    kid_price: str = "1,000,000"
    start_date: date
    end_date: date
    seat: int
    tour_desc: Optional[str]

    class Config:
        orm_mode = True


class Place(BaseModel):
    place_id: str
    place_name: str
    city_id: str
    place_desc: str

    class Config:
        orm_mode = True
