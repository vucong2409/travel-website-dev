from os import link
from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime

from sqlalchemy import orm
from sqlalchemy.log import class_logger
from sqlalchemy.sql.elements import ClauseList
from database import Base

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

class UserAlter(BaseModel):
    login_password: Optional[str] = None
    nationality: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    email: Optional[str] = None

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
    tour_title: str
    tour_bg_img: Optional[str]

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
    tour_title: str
    tour_bg_img: Optional[str]

    class Config:
        orm_mode = True


class Place(BaseModel):
    place_id: str
    place_name: str
    city_id: str
    place_desc: str
    image_link: str

    class Config:
        orm_mode = True

class Order(BaseModel):
    order_id: int
    order_date: date
    order_detail: str
    user_id: int
    confirmed: int

class OrderDetails(BaseModel):
    order_id: int
    tour_id: str
    adult_number: int
    kid_number: int
    adult_price: int
    kid_price: int
    customer_id: int

class Booking(BaseModel):
    booking_id: int
    order_id: int
    customer_id: int

class OrderForm(BaseModel):
    order_date: date
    order_detail: str
    tour_id: str
    adult_number: int
    kid_number: int
    adult_price: int
    kid_price: int

class Routes(BaseModel):
    route_id: Optional[int]
    route_name: str
    route_desc: str
    step_number: int
    tour_id: str

    class Config: 
        orm_mode = True
    
class Images(BaseModel):
    id: Optional[int]
    name: str
    link: str
    tour_id: str

    class Config: 
        orm_mode = True