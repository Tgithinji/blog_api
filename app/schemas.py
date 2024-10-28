from pydantic import BaseModel
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
