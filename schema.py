from pydantic import BaseModel, field_validator
from typing import List

from fastapi import HTTPException, UploadFile


class Sign(BaseModel):
    user_id: str
    user_pw: str

    @field_validator("user_id", "user_pw")
    @classmethod
    def check_field(cls, v):
        if not v or v.isspace():
            raise HTTPException(status_code=422, detail="필수 항목을 입력해주세요.")
        return v

    @field_validator("user_pw")
    @classmethod
    def check_password(cls, v):
        if len(v) < 8:
            raise HTTPException(
                status_code=422, detail="8자리 이상의 영문과 숫자를 포함해주세요."
            )
        if not any(char.isdigit() for char in v):
            raise HTTPException(
                status_code=422, detail="8자리 이상의 영문과 숫자를 포함해주세요."
            )

        if not any(char.isalpha() for char in v):
            raise HTTPException(
                status_code=422, detail="8자리 이상의 영문과 숫자를 포함해주세요."
            )
        return v


class TypingDataFrame(BaseModel):
    _id: str
    wpm: float
    acc: float
    mode: str
    testDuration: float
    language: str
    timestamp: int


class FilterType(BaseModel):
    user_id: str
    language: List[str] = []
    mode: List[str] = []


class TypingData(BaseModel):
    wpm: float
    acc: float
