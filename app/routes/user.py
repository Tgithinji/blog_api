from fastapi import APIRouter, status, HTTPException, Depends
from app import models, schemas, password_hash
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
""" Users routes
"""

router = APIRouter(prefix="/users", tags=['Users'])


# create user
@router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check if user exists and raise an exception if true
    user_exists = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    user.password = password_hash.hash_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

 
# fetch a user's detail
@router.get("/{id}", response_model=schemas.UserWithPosts)
def get_user(id: int, db: Session = Depends(get_db)):
    # user = db.query(models.User).filter(models.User.id == id).first()
    following_query = db.query(func.count(models.Follow.follower_id)).filter(
        models.Follow.follower_id == id
    )
    followers_query = db.query(func.count(models.Follow.following_id)).filter(
        models.Follow.following_id == id
    )
    result = db.query(
        models.User,
        func.count(models.Post.author_id).label("posts"),
        following_query.scalar_subquery().label("following"),
        followers_query.scalar_subquery().label("followers")
    ).outerjoin(
        models.Post, models.Post.author_id == models.User.id,
    ).filter(models.User.id == id).group_by(models.User.id).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    return result


# fetch all users
@router.get("/", response_model=List[schemas.UserWithPosts])
def get_users(db: Session = Depends(get_db)):
    # users = db.query(models.User).all()
    following_query = db.query(func.count(models.Follow.follower_id)).filter(
        models.Follow.follower_id == models.User.id
    )
    followers_query = db.query(func.count(models.Follow.following_id)).filter(
        models.Follow.following_id == models.User.id
    )
    result = db.query(
        models.User,
        func.count(models.Post.author_id).label("posts"),
        following_query.scalar_subquery().label("following"),
        followers_query.scalar_subquery().label("followers")
    ).outerjoin(
        models.Post, models.Post.author_id == models.User.id,
    ).group_by(models.User.id).all()

    return result
