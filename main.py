from openai import OpenAI
import router.typing_router as typing_router
import router.user_router as user_router
from crud import typing_crud

from sqlalchemy.orm import Session

import models
from database import get_db, engine
from schema import FilterType, UserForm

import os
from dotenv import load_dotenv

from typing_extensions import Annotated

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from security import verify_access_token


models.Base.metadata.create_all(bind=engine)

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_WEEKS = float(os.getenv("REFRESH_TOKEN_EXPIRE_WEEKS"))
app = FastAPI()

app.include_router(typing_router.app, tags=["typing"])
app.include_router(user_router.app, tags=["user"])

origins = [
    "https://monkeyfinger.netlify.app",
    ".netlify.app",
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


client = OpenAI(
    organization="org-MTh1QeshOBBE0hOZAi5z9Mfo",
    project="proj_CH1M2LPgCzpMvmS2W4TJD4Fj",
)

load_dotenv()
client.api_key = os.getenv("OPENAI_API_KEY")


@app.post("/advice")
def advice(
    user: Annotated[UserForm, Depends(verify_access_token)],
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
