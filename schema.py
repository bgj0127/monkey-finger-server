from pydantic import BaseModel, field_validator
from typing import List

from fastapi import HTTPException


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    userId: str | None = None


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


class FilterType(BaseModel):
    language: List[str] = []
    mode: List[str] = []


class TypingData(BaseModel):
    wpm: float
    acc: float
