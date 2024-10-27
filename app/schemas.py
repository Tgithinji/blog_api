from pydantic import BaseModel


# structure of a request or response
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
