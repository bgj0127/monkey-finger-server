from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db

import os
from dotenv import load_dotenv
from jose import jwt, JWTError, ExpiredSignatureError
from typing_extensions import Annotated
from schema import TokenData
from crud import user_crud

from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login", scheme_name="Token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def auth_user(username: str, password: str, db: Session = Depends(get_db)):
    user = user_crud.get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.user_pw):
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


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=5)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_access_token(
    request: Request,
    response: Response,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )

    print(request.cookies.get("access_token"))
    print(request.cookies.get("refresh_token"))

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        print("Access 토큰 만료")
        response.delete_cookie("access_token")
        refresh_token = request.cookies.get("refresh_token")
        new_access_token = verify_refresh_token(token=refresh_token)
        payload = jwt.decode(new_access_token, SECRET_KEY, algorithms=[ALGORITHM])
    else:
        credential_exception
    user_id: str = payload.get("sub")
    if not user_id:
        raise credential_exception
    token_data = TokenData(user_id=user_id)

    user = user_crud.get_user(token_data.user_id, db)
    if not user:
        raise credential_exception

    return user


def verify_refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_id}, expires_delta=access_token_expires
        )
        if not user_id:
            raise credential_exception
    except JWTError:
        credential_exception
    else:
        print("Refresh 토큰 만료")

    return access_token


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
