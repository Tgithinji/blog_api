from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app import models, password_hash, jwt_handler, schemas
"""Authentication routes
"""

router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)
def login(
    user_creds: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # user can login either using their email or username
    # check if either matches with credentials provided
    user = db.query(models.User).filter(
        or_(
            models.User.email == user_creds.username,
            models.User.username == user_creds.username
        )
    ).first()

    # raise an exception if either of the above checks fails
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )

    # check if password matches
    verify_password = password_hash.verify_password(user_creds.password, user.password)
    # if not raise an exception
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )

    # create and return a token
    access_token = jwt_handler.create_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
