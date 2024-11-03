from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
TOKEN_EXPIRY = settings.token_expiry


def create_token(data: dict):
    # create a copy of the data so as not to mess up the original data
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRY
    )
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return access_token


def verify_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get('user_id')

        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credential_exception
    return token_data


# verify if the token is valid and use it to secure routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Cannot validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token = verify_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
