from fastapi import APIRouter, status, HTTPException, Response, Depends
from app import models, schemas
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List
""" Posts routes
"""

router = APIRouter(prefix="/posts", tags=['Posts'])


# get posts path
@router.get("/", response_model=List[schemas.PostReturned])
def get_posts(db: Session = Depends(get_db)):
    """Get posts
    """
    all_posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts""")
    # all_posts = cursor.fetchall()
    return all_posts


# Create posts path
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostReturned)
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
@router.get("/{id}", response_model=schemas.PostReturned)
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
    return post


# Update a post
@router.put("/{id}", response_model=schemas.PostReturned)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id ==  id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"id {id} does not exist")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"id {id} does not exist")

    post_query.delete(synchronize_session=False)
    db.commit()    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
