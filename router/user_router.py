from sqlalchemy.orm import Session
from database import get_db
from schema import UserForm
from crud import user_crud
import os
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request


ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

load_dotenv()
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


@app.get("/logout", description="유저 - 로그아웃")
def logout(response: Response, request: Request):
    access_token = request.cookies.get("access_token")
    print(access_token)
    # 쿠키 삭제
    response.delete_cookie(key="access_token")

    return HTTPException(status_code=status.HTTP_200_OK, detail="Logout successful")
