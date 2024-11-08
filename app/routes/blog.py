from fastapi import APIRouter, status, HTTPException, Response, Depends
from app import models, schemas, jwt_handler
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
""" Posts routes
"""

router = APIRouter(prefix="/posts", tags=['Posts'])


# get posts path
@router.get("/", response_model=List[schemas.PostWithComments])
def get_posts(
    db: Session = Depends(get_db),
    search: str = "",
    limit: int = 10,
    skip: int = 0
):
    """Get posts
    """

    all_posts = db.query(
        models.Post,
        func.count(models.Comments.post_id).label("comments"),
        func.count(models.Likes.post_id).label("likes")
    ).outerjoin(
        models.Comments, models.Comments.post_id == models.Post.id,
    ).outerjoin(
        models.Likes, models.Likes.post_id == models.Post.id
    ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()

    return all_posts


# Create posts path
@router.post(
        "/", status_code=status.HTTP_201_CREATED,
        response_model=schemas.PostReturned
)
def create_posts(
    post: schemas.Post,
    current_user: int = Depends(jwt_handler.get_current_user),
    db: Session = Depends(get_db)
):
    new_post = models.Post(author_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Get one post
@router.get("/{id}", response_model=schemas.PostWithComments)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(
        models.Post,
        func.count(models.Comments.post_id).label("comments"),
        func.count(models.Likes.post_id).label("likes")
    ).outerjoin(
        models.Comments, models.Comments.post_id == models.Post.id,
    ).outerjoin(
        models.Likes, models.Likes.post_id == models.Post.id,
    ).group_by(models.Post.id).filter(models.Post.id == id).first()

    # if post is not found raise a HTTP exception
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    return post


# Update a post
@router.put("/{id}", response_model=schemas.PostReturned)
def update_post(
    id: int, post: schemas.Post,
    current_user: int = Depends(jwt_handler.get_current_user),
    db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"id {id} does not exist"
        )

    # logic to check if user is only updates own post
    if post_query.first().author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not authorized"
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(
    id: int,
    current_user: int = Depends(jwt_handler.get_current_user),
    db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"id {id} does not exist"
        )

    # logic to check if user is only deleting own post
    if post_query.first().author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not authorized"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
