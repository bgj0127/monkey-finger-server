from sqlalchemy import asc, or_
from sqlalchemy.orm import Session
import pandas as pd

from models import Typing


def insert_typing_data(user_id: str, typing_df: pd.DataFrame, db: Session):

    # 데이터 insert문 작성하기
    for i in range(typing_df.shape[0]):
        new_data = (
            db.query(Typing)
            .filter(Typing.typing_id == typing_df.iloc[i]["_id"])
            .first()
        )
        if new_data:
            continue
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

    lan = [i + "%" for i in language]

    lists = (
        db.query(Typing)
        .where(Typing.user_id == user_id)
        .where(or_(*[Typing.language.like(pattern) for pattern in lan]))
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
