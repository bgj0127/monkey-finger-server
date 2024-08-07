from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db

import os
from jose import jwt, JWTError
from typing_extensions import Annotated
from schema import TokenData
from crud import user_crud

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def auth_user(username: str, password: str, db: Session = Depends(get_db)):
    user = user_crud.get_user(username, db)
    if not user:
        return False
    if not user_crud.verify_password(password, user.user_pw):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_access_token(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userId: str = payload.get("sub")
        if userId is None:
            raise credential_exception
        token_data = TokenData(userId=userId)
    except JWTError:
        raise credential_exception

    user = user_crud.get_user(token_data.userId, db)
    if not user:
        raise credential_exception
    return user
