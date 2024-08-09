from sqlalchemy.orm import Session
from database import get_db
from schema import UserForm, Token
from crud import user_crud
from typing_extensions import Annotated

import os
from dotenv import load_dotenv
from datetime import timedelta


from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from security import auth_user, create_access_token, create_refresh_token


load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_WEEKS = float(os.getenv("REFRESH_TOKEN_EXPIRE_WEEKS"))
app = APIRouter(prefix="/user")


@app.post("/register", description="유저 - 회원가입")
def register_new_user(user: UserForm, db: Session = Depends(get_db)):
    new_user = user_crud.get_user(user.user_id, db)

    if new_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    user_crud.insert_user(user, db)

    return HTTPException(status_code=status.HTTP_200_OK, detail="Register successful")


@app.post("/login", description="유저 - 로그인", response_model=Token)
def login(
    login_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = auth_user(login_form.username, login_form.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(weeks=REFRESH_TOKEN_EXPIRE_WEEKS)
    access_token = create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.user_id}, expires_delta=refresh_token_expires
    )

    response = JSONResponse(content={"message": "cookieeeeeeeee"})

    response.set_cookie(
        key="access_token",
        value=access_token,
        samesite="none",
        secure=True,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        samesite="none",
        secure=True,
    )

    return Token(access_token=access_token, refresh_token=refresh_token)


@app.get("/logout", description="유저 - 로그아웃")
def logout(request: Request):
    access_token = request.cookies.get("access_token")
    print(access_token)
    # 쿠키 삭제
    response = JSONResponse(content={"message": "cookieeeeeeeee"})

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return HTTPException(status_code=status.HTTP_200_OK, detail="Logout successful")
