from jose import jwt, JWTError
from datetime import datetime, timedelta


SECRET_KEY = '3e32d321dcb61f8dd0eff0f56ebaffffd8621bf0bd66c36e1e8a9d8e0c6add17'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return access_token