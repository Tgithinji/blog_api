from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# structure of th user details
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# login structure
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# structure of a request
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    pass


# structure of a response
class PostReturned(PostBase):
    id: int
    created_at: datetime
    author: UserResponse

    class Config:
        from_attributes = True


# define schemas for tokens
class Token(BaseModel):
    access_token: str
    token_type: str


# schema for token data
class TokenData(BaseModel):
    id: Optional[str]
