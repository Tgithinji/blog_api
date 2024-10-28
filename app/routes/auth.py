from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app import schemas, models, utils, jwt_handler
"""Authentication routes
"""

router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(
    user_creds: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        or_(
            models.User.email == user_creds.username,
            models.User.username == user_creds.username
        )
    ).first()
    verify_password = utils.verify_password(user_creds.password, user.password)

    if not user or not verify_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials"
        )
    
    # create and return a token
    access_token = jwt_handler.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
    
    