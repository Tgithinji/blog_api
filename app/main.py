from fastapi import FastAPI, status, HTTPException, Response, Depends
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from . import models, schemas
from .database import init_db, get_db
from sqlalchemy.orm import Session

app = FastAPI()

# initialize database tables
init_db()


# structure of a request or response
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


@app.get("/sqlachemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


# get posts path
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    """Get posts
    """
    all_posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts""")
    # all_posts = cursor.fetchall()
    return {"data": all_posts}


# Create posts path
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content)
    #     VALUES (%s, %s) RETURNING *""",
    #     (post.title, post.content)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Get one post
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """SELECT * FROM posts
    #     WHERE id = %s""", (str(id),)
    # )
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    # if post is not found raise a HTTP exception
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    return {"post_details": post}


# Update a post
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id ==  id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"id {id} does not exist")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


# Delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"id {id} does not exist")

    post_query.delete(synchronize_session=False)
    db.commit()    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
