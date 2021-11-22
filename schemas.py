from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime

from sqlalchemy import orm

class Token(BaseModel):
    access_token: str
    token_type: str

class Login_Form(BaseModel):
    login_username: str
    login_password: str

class Login(Login_Form):
    login_id: Optional[int]
    login_role_id: Optional[int]

class TourBase(BaseModel):
    tour_id: str
    place_id: str
    tourguide_id: str
    type_id: str
    transport: str
    departure_place: str
    adult_price: str
    kid_price: str
    start_date: date
    end_date: date
    seat: int
    tour_desc: str

    class Config:
        orm_mode = True


class TourID(BaseModel):
    tour_id: str


class Tour(TourBase):
    pass

    class Config:
        orm_mode: True
