from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
"""Structure of the responses and request details
"""


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


class UserWithPosts(BaseModel):
    User: UserResponse
    posts: int


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


class PostWithComments(BaseModel):
    Post: PostReturned
    comments: int


# define schemas for tokens created
class Token(BaseModel):
    access_token: str
    token_type: str


# schema for token data
class TokenData(BaseModel):
    id: Optional[str]


# schema for comments
class CommentsCreate(BaseModel):
    content: str

class CommentsResponse(CommentsCreate):
    id: int
    post_id: int
    user_id: int
    created_at: datetime
