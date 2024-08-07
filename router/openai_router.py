from sqlalchemy.orm import Session
from database import get_db

from fastapi import APIRouter, Depends, HTTPException, status

app = APIRouter(prefix="/openai")


# 값을 어떻게 넘겨줄 것인가.
# DB 조회는 어떻게 할것인가
@app.get("/advice/{user_id}")
def read_openai_advice(user_id: str, db: Session = Depends(get_db)):
    pass
