from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg2.extras import RealDictCursor
import psycopg2
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Continue only when database is connected
while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='blog_api',user='postgres',
            password='password', cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print('Database connection successful')
        break
    except Exception as error:
        print('Connection to database failed')
        print('Error: ', error)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

# get posts path
@app.get("/posts")
def get_posts():
    """Get posts
    """
    cursor.execute("""SELECT * FROM posts""")
    all_posts = cursor.fetchall()
    return {"data": all_posts}


# Create posts path
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content)
        VALUES (%s, %s) RETURNING *""",
        (post.title, post.content)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# Get one post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(
        """SELECT * FROM posts
        WHERE id = %s""", (str(id),)
    )
    post = cursor.fetchone()
    # if post is not found raise a HTTP exception
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    return {"post_details": post}


# Update a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts
        SET title = %s, content = %s, published = %s
        WHERE id = %s
        RETURNING *
        """,
        (post.title, post.content, post.published, str(id),)
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"id {id} does not exist")
    return {"data": updated_post}


# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"id {id} does not exist")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
