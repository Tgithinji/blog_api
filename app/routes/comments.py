from fastapi import APIRouter,status, Depends, HTTPException
from app import schemas, database, jwt_handler, models
from sqlalchemy.orm import Session
from typing import List
"""Comments routes
"""

router = APIRouter(
    prefix="/posts",
    tags=['Comments']
)


# route to create a comment
@router.post(
        "/{id}/comments",
        status_code=status.HTTP_201_CREATED,
        response_model=schemas.CommentsResponse
)
def create_comment(
    id: int,
    comment: schemas.CommentsCreate,
    db : Session = Depends(database.get_db),
    current_user: int = Depends(jwt_handler.get_current_user)
):
    # find the post the user wants to commented on
    post = db.query(models.Post).filter(
        models.Post.id == id
    ).first()
    # if post was not found raise an exception
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    
    new_comment = models.Comments(
        user_id=current_user.id,
        post_id=id,
        **comment.model_dump()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


# route to get comments of a certain post
@router.get(
        "/{id}/comments",
        response_model=List[schemas.CommentsResponse]
)
def get_comments_by_post(
    id: int,
    db : Session = Depends(database.get_db),
):
     # find the post we want fetch comments for
    post = db.query(models.Post).filter(
        models.Post.id == id
    ).first()
    # if post was not found raise an exception
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )
    
    # fetch comments by post id
    comments = db.query(models.Comments).filter(
        models.Comments.post_id == id
    ).all()
    return comments


# route to delete a comment
@router.delete(
    "/{post_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_comment(
    post_id: int,
    comment_id: int,
    current_user: int = Depends(jwt_handler.get_current_user),
    db: Session = Depends(database.get_db)
):
     # check if post we want to delete comment for exists
    post = db.query(models.Post).filter(
        models.Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist"
        )
    
    comment = db.query(models.Comments).filter(
        models.Comments.id == comment_id
    ).first()

    # check if comment exists
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} not found"
        )
    
    # check to make sure user deletes own posts only
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation is forbidden"
        )
    
    db.delete(comment)
    db.commit()
