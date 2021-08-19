from pydantic import BaseModel
from typing import Optional


class Todo(BaseModel):
    todo_id: str
    title: str
    description: str


class User(BaseModel):
    name: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
