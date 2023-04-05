
from pydantic import BaseModel


class UserItem(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
