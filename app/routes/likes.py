from fastapi import APIRouter, status, Depends, HTTPException
from app import database, jwt_handler, models
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=['likes']
)


@router.post("/{post_id}/likes", status_code=status.HTTP_201_CREATED)
def like_post(
    post_id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(jwt_handler.get_current_user)
):
    # find the post
    post = db.query(models.Post).filter(
        models.Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {post_id} does not exist"
        )
    
    # check if user had liked post
    like_query = db.query(models.Likes).filter(
        models.Likes.post_id == post_id,
        models.Likes.user_id == current_user.id
    )
    if like_query.first():
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "You unliked post"}
    
    # else add like
    like = models.Likes(post_id=post_id, user_id=current_user.id)
    db.add(like)
    db.commit()
    return {"message": "You liked post"}


@router.post("/{post_id}/comments/{com_id}/likes", status_code=status.HTTP_201_CREATED)
def like_comment(
    post_id: int,
    com_id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(jwt_handler.get_current_user)
):
    # find the post
    post = db.query(models.Post).filter(
        models.Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} does not exist"
        )
    
    # find the comment
    comment = db.query(models.Comments).filter(
        models.Comments.id == com_id
    ).first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with {com_id} does not exist"
        )
    
    # check if user had liked post
    like_query = db.query(models.Likes).filter(
        models.Likes.comment_id == com_id,
        models.Likes.user_id == current_user.id
    )
    if like_query.first():
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "You unliked comment"}
    
    # else add like
    like = models.Likes(comment_id=com_id, user_id=current_user.id)
    db.add(like)
    db.commit()
    return {"message": "You liked comment"}
