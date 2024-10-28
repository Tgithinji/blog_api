from pydantic import BaseModel, EmailStr
from datetime import datetime


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

    class Config:
        from_attributes = True

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
