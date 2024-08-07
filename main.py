from openai import OpenAI
import router.typing_router as typing_router
import router.user_router as user_router
from crud import typing_crud

from sqlalchemy.orm import Session

import models
from database import get_db, engine
from schema import Token, FilterType, Sign

import os
from dotenv import load_dotenv

from typing_extensions import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from security import create_access_token, auth_user, verify_access_token

models.Base.metadata.create_all(bind=engine)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

app.include_router(typing_router.app, tags=["typing"])
app.include_router(user_router.app, tags=["user"])

origins = [
    "https://monkeyfinger.netlify.app",
    "https://master--monkeyfinger.netlify.app",
]
# origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return "hello"


@app.post("/token", description="유저 - 로그인", response_model=Token)
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
    access_token = create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="Bearer")


client = OpenAI(
    organization="org-MTh1QeshOBBE0hOZAi5z9Mfo",
    project="proj_CH1M2LPgCzpMvmS2W4TJD4Fj",
)

load_dotenv()
client.api_key = os.getenv("OPENAI_API_KEY")


@app.post("/advice")
def advice(
    user: Annotated[Sign, Depends(verify_access_token)],
    filter: FilterType,
    db: Session = Depends(get_db),
):
    result = typing_crud.list_filtered_data(
        user.user_id, filter.language, filter.mode, db
    )

    model = "gpt-4o-mini"
    query = f"{result}"
    messages = [
        {
            "role": "system",
            "content": "타자연습 데이터를 매우 상세하게 분석해서 간단명료하게 알려줘. 주어진 데이터는 wpm, acc, 테스트 소요 시간, 테스트 모드야. 말투는 친근한 비서처럼.",
        },
        {"role": "user", "content": query},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        max_tokens=512,
        frequency_penalty=1.2,
    )
    return response.choices[0].message.content
