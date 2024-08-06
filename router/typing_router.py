from sqlalchemy.orm import Session
from database import get_db
from crud import typing_crud
import pandas as pd
from schema import FilterType

from fastapi import APIRouter, Depends, UploadFile, HTTPException, status

app = APIRouter(prefix="/typing")


@app.get("/test")
def typing_test():
    return "test"


@app.post("/filter", description="타자 기록 - 데이터 조회")
def read_filtered_data(filter: FilterType, db: Session = Depends(get_db)):
    print(filter.user_id, filter.language, filter.mode)
    return typing_crud.list_filtered_data(
        filter.user_id, filter.language, filter.mode, db
    )


@app.post("/upload", description="타자 기록 - 데이터 삽입")
def write_typing_data(
    user_id: str, typing_data: UploadFile, db: Session = Depends(get_db)
):
    typing_df = pd.read_csv(typing_data.file)
    typing_data.file.close()
    if "wpm" not in typing_df.columns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MonkeyType csv 파일만 업로드 가능합니다.",
        )
    res = typing_crud.insert_typing_data(user_id, typing_df, db)

    if not res:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 데이터입니다."
        )
    return HTTPException(status_code=status.HTTP_200_OK, detail="데이터 업데이트 성공")
