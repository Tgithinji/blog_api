from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    body: str
    published: bool = True
    rating: Optional[int] = True


my_posts = [
    {'title': 'First post', 'body': 'Hello there','id': 1},
    {'title': 'Second post', 'body': 'Jambo', 'id': 2}
]


# function to find a post by id
def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        

# function to find an index of a post with given id
def find_index(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

# get posts path
@app.get("/posts")
def get_posts():
    """Get posts
    """
    return {"data": my_posts}


# Create posts path
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    #turn the received post to a dict
    post_dict = post.dict()
    # assign a random id and append to the list of posts
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# Get one post
@app.get("/posts/{id}")
def get_post(id: int):
    # find the post associated with the id
    post = find_post(id)
    # if post is not found raise a HTTP exception
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    return {"post_details": post}


# Update a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # find index of the post to be updated
    index = find_index(id)
    # if not found raise an exception
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    # if it exists replace it with the given post
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post}


# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find index of post by id
    index = find_index(id)
    # if not found raise an exception
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    # else delete it
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
