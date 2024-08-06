from sqlalchemy.orm import Session
from database import get_db
from schema import Sign
from crud import user_crud

from fastapi import APIRouter, Depends, HTTPException, status

app = APIRouter(prefix="/user")


@app.post("/register", description="유저 - 회원가입")
def register_new_user(user: Sign, db: Session = Depends(get_db)):
    new_user = user_crud.get_user(user.user_id, db)

    if new_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    user_crud.insert_user(user, db)

    return HTTPException(status_code=status.HTTP_200_OK, detail="Register successful")


@app.post("/login", description="유저 - 로그인")
def login(login_form: Sign, db: Session = Depends(get_db)):
    user = user_crud.get_user(login_form.user_id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user or password"
        )

    res = user_crud.verify_password(login_form.user_pw, user.user_pw)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user or password"
        )

    return {
        "userId": user.user_id,
        "result": HTTPException(
            status_code=status.HTTP_200_OK, detail="Login successful"
        ),
    }
