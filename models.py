from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import VARCHAR, DATE, INTEGER
from .database import Base


class Tour(Base):
    __tablename__ = "tours"

    tour_id = Column(VARCHAR(10), primary_key=True, nullable=False)
    place_id = Column(VARCHAR(10), ForeignKey("places.place_id"), nullable=False)
    tourguide_id = Column(
        VARCHAR(10), ForeignKey("tourguides.tourguide_id"), nullable=False
    )
    type_id = Column(VARCHAR(10), ForeignKey("types.type_id"), nullable=False)
    transport = Column(VARCHAR(10), nullable=False)
    departure_place = Column(VARCHAR(10), nullable=False)
    adult_price = Column(VARCHAR(20), nullable=False)
    kid_price = Column(VARCHAR(20), nullable=False)
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=False)
    seat = Column(INTEGER, nullable=False)
    tour_desc = Column(VARCHAR(100), default=null)


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        INTEGER, ForeignKey("login.login_id"), primary_key=True, nullable=False
    )
    user_name = Column(VARCHAR(50), nullable=False)  # unique?
    nationality = Column(VARCHAR(50), nullable=False)
    phone = Column(VARCHAR(50), nullable=False)
    address = Column(VARCHAR(50), nullable=False)
    city = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(50), nullable=False)  # unique?


class Login(Base):
    __tablename__ = "login"

    login_id = Column(INTEGER, primary_key=True, autoincrement=True)
    login_role_id = Column(VARCHAR(10), ForeignKey("roles.role_id"), nullable=False)
    login_user_name = Column(VARCHAR(50), nullable=False)
    login_user_password = Column(VARCHAR(50), nullable=False)


class Permission(Base):
    __tablename__ = "permission"

    per_id = Column(VARCHAR(10), primary_key=True, nullable=False)
    per_role_id = Column(VARCHAR(10), ForeignKey("roles.role_id"), nullable=False)
    per_name = Column(VARCHAR(50), nullable=False)
    per_module = Column(VARCHAR(50), nullable=False)


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(VARCHAR(10), primary_key=True, nullable=False)
    role_name = Column(VARCHAR(20), nullable=False)
    role_desc = Column(VARCHAR(20), nullable=False)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    order_date = Column(DATE, nullable=False)  # datetime
    order_detail = Column(VARCHAR(50), default=null)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)


class Orderdetail(Base):
    __tablename__ = "orderdetails"

    order_id = Column(
        INTEGER,
        ForeignKey("orders.order_id"),
        nullable=False,
        autoincrement=True,
        primary_key=True,
    )
    tour_id = Column(
        VARCHAR(10), ForeignKey("tours.tour_id"), nullable=False, primary_key=True
    )
    adult_number = Column(INTEGER, nullable=False)
    kid_number = Column(INTEGER, nullable=False)
    adult_price = Column(INTEGER, nullable=False)
    kid_price = Column(INTEGER, nullable=False)
    customer_id = Column(INTEGER, nullable=False)


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    customer_name = Column(VARCHAR(50), nullable=False)
    sex = Column(VARCHAR(10), nullable=False)
    birthday = Column(DATE, nullable=False)
    nationality = Column(VARCHAR, nullable=False)
    passport = Column(VARCHAR(100), default=null)
    address = Column(VARCHAR(100), nullable=False)
    city = Column(VARCHAR(50), nullable=False)
    email = Column(VARCHAR(50), nullable=False)
    phone = Column(VARCHAR(10), nullable=False)


class Place(Base):
    __tablename__ = "places"

    place_id = Column(VARCHAR(10), primary_key=True, nullable=False)
    place_name = Column(VARCHAR(50), nullable=False)
    city_id = Column(VARCHAR(10), ForeignKey("cities.city_id"), nullable=False)
    place_desc = Column(VARCHAR(100), default=null)


class City(Base):
    __tablename__ = "cities"

    city_id = Column(VARCHAR(10), primary_key=True, nullable=False)
    city_name = Column(VARCHAR(50), nullable=False)


class Type(Base):
    __tablename__ = "types"

    type_id = Column(VARCHAR(10), primary_key=True, nullable=False)
    type_name = Column(VARCHAR(50), nullable=False)
    type_desc = Column(VARCHAR(100), default=null)


class Tourguide(Base):
    __tablename__ = "tourguides"

    tourGuide_id = Column(VARCHAR(10), primary_key=True, nullable=False)
    guide_name = Column(VARCHAR(50), nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(VARCHAR(10), nullable=False)
    phone = Column(INTEGER, nullable=False)  # varchar
    description = Column(VARCHAR(100), nullable=False)


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(INTEGER, ForeignKey("users.user_id"), nullable=False)
    tour_id = Column(VARCHAR(10), ForeignKey("tours.tour_id"), nullable=False)
    rating = Column(INTEGER(5), nullable=False)
    comment = Column(VARCHAR(100), nullable=False)


class Booking(Base):
    __tablename__ = "booking"

    booking_id = Column(
        INTEGER,
        ForeignKey("orderdetails.order_id"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    order_id = Column(INTEGER, nullable=False)
    customer_id = Column(INTEGER, ForeignKey("customers.customer_id"), nullable=False)
