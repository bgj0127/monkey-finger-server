from sqlalchemy import asc, or_
from sqlalchemy.orm import Session
from pydantic import TypeAdapter
from typing import List
import pandas as pd

from models import Typing
from schema import TypingDataFrame


def insert_typing_data(user_id: str, typing_df: pd.DataFrame, db: Session):

    # 데이터 insert문 작성하기
    for i in range(typing_df.shape[0]):
        # print(typing_df.iloc[i])
        new_data = (
            db.query(Typing)
            .filter(Typing.typing_id == typing_df.iloc[i]["_id"])
            .first()
        )

        if new_data:
            print("중복 데이터")
        data = Typing(
            typing_id=typing_df.iloc[i]["_id"],
            wpm=float(typing_df.iloc[i]["wpm"]),
            acc=float(typing_df.iloc[i]["acc"]),
            test_mode=typing_df.iloc[i]["mode"],
            test_duration=float(typing_df.iloc[i]["testDuration"]),
            language=typing_df.iloc[i]["language"],
            timestamp=int(typing_df.iloc[i]["timestamp"]),
            user_id=user_id,
        )
        db.add(data)
    db.commit()
    return "데이터 insert 완료"


def list_filtered_data(user_id, language, mode, db: Session):
    d = {
        "wpm": [],
        "acc": [],
        "time": [],
        "mode": [],
        "language": [],
        "duration": [],
    }

    lists = (
        db.query(Typing)
        .where(Typing.user_id == user_id)
        .where(or_(*[Typing.language.like(pattern) for pattern in language]))
        .where(Typing.test_mode.in_(mode))
        .order_by(asc(Typing.timestamp))
        .all()
    )

    for row in lists:
        d["wpm"].append(row.wpm)
        d["acc"].append(row.acc)
        d["time"].append(row.timestamp)
        d["mode"].append(row.test_mode)
        d["language"].append(row.language)
        d["duration"].append(row.test_duration)

    return d
