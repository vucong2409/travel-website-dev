from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class Login_Form(BaseModel):
    login_username: str
    login_password: str

class Login(Login_Form):
    login_id: Optional[int]
    login_role_id: Optional[int]