from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.elements import True_
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.schema import Index, UniqueConstraint

import database

class Login(database.Base):
    __tablename__ = 'login'
    login_id = Column(Integer, primary_key=True, index=True)
    login_role_id = Column(Integer)
    login_username = Column(String(100), unique=True)
    login_password = Column(String(100), unique=True)
