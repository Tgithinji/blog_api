from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database, jwt_handler, models

router = APIRouter(
    prefix="/users",
    tags=["follows"]
)


@router.post("/{following_id}/follow", status_code=status.HTTP_201_CREATED)
def follow_user(
    following_id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(jwt_handler.get_current_user)
):
    # make sure users cannot follow themselves
    if following_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow yourself"
        )
    # check if the user to be followed exists
    user = db.query(models.User).filter(
        models.User.id == following_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {following_id} does not exist"
        )
    # check if user already follows
    follow = db.query(models.Follow).filter_by(
        follower_id=current_user.id,
        following_id=following_id
    ).first()
    if follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You already follow user with id {following_id}"
        )
    
    new_follow = models.Follow(following_id=following_id, follower_id=current_user.id)
    db.add(new_follow)
    db.commit()
    return {"message": f"You followed user {following_id}"}


@router.delete("/{following_id}/unfollow", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(
    following_id: int,
    db: Session=Depends(database.get_db),
    current_user: int = Depends(jwt_handler.get_current_user)
):
    # check if the user to be followed exists
    user = db.query(models.User).filter(
        models.User.id == following_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {following_id} does not exist"
        )
    
    follow_query = db.query(models.Follow).filter_by(
        follower_id=current_user.id,
        following_id=following_id
    )
    if not follow_query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You do not follow user with id {following_id}"
        )
    
    follow_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"You unfollowed user {following_id}"}
    