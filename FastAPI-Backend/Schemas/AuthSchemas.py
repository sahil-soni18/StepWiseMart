
from pydantic import BaseModel
from typing import Optional

class UserCred(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserInDB(UserCred):
    password: str
