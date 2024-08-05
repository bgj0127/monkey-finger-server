from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Path
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from DB_Control import connDB, filtered_data, view
from openai import OpenAI
import os
from dotenv import load_dotenv

engine, table, m = connDB("MONKEY_FINGER")
app = FastAPI()

origins = [
    "http://localhost:5173/",
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


@app.get("/", status_code=200)
def root():
    return "hello"


class FilterType(BaseModel):
    language: List[str] = []
    mode: List[str] = []


@app.post("/filter")
def search_filter(filter_type: FilterType):
    lanFilter = filter_type.language
    modeFilter = filter_type.mode
    with engine.connect() as conn:
        try:
            return filtered_data(table, conn, lanFilter, modeFilter)
        except HTTPException as e:
            print(e)
            return {"data": {"None"}, "status": e.status_code}
    # return {"language": filter_type.language, "mode": filter_type.mode}


class TypingData(BaseModel):
    wpm: float
    acc: float


client = OpenAI(
    organization="org-MTh1QeshOBBE0hOZAi5z9Mfo",
    project="proj_CH1M2LPgCzpMvmS2W4TJD4Fj",
)

load_dotenv()
client.api_key = os.getenv("OPENAI_API_KEY")


# 이것도 get으로 변경하자.
@app.get("/advice")
# 이거 그냥 DB 조회로 하자. body로 데이터 받지 말고.
def advice():
    engine, view_table, m = connDB("MONKEY_FINGER_VIEW")

    with engine.connect() as conn:
        d = view(view_table, conn)
    model = "gpt-4o-mini"
    query = f"{d}"
    messages = [
        {
            "role": "system",
            "content": 'Analyzing the results of typing practice records. Advice must required. must json object. keys are english, values are korean. { "average_speed": "", "average_accuracy": "", "average_duration": "", "speed_trend": "상승/감소/유지", "accuracy_trend": "상승/감소/유지", "stability":"", "advice": "kindly advice" }',
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

    # @app.post("/uploadfile")
    # def upload_file(file: UploadFile):
    #     df = pd.read_csv(file.file)
    #     file.file.close()
    #     if "wpm" not in df.columns:
    #         return {"res": "Monkey Type csv 파일만 넣어주세요"}
    #     df.loc[df["isPb"].isna(), "isPb"] = 0
    #     df.loc[df["isPb"] == True, "isPb"] = 1
    #     for i in range(df.shape[0]):
    #         insert_data = f"""
    #         merge into monkey_type
    #         using dual
    #         on (id='{df.iloc[i]['_id']}')
    #         when not matched then
    #             insert
    #             (
    #                 id, is_pb, wpm, acc, test_mode, test_mode2, test_duration, language, timestamp
    #             )
    #             values(
    #             '{df.iloc[i]['_id']}',
    #             {df.iloc[i]['isPb']},
    #             {df.iloc[i]['wpm']},
    #             {df.iloc[i]['acc']},
    #             '{df.iloc[i]['mode']}',
    #             '{df.iloc[i]['mode2']}',
    #             {df.iloc[i]['testDuration']},
    #             '{df.iloc[i]['language']}',
    #             {df.iloc[i]['timestamp']}
    #         )
    #         """
    #         try:
    #             cur.execute(insert_data)
    #             cur.execute("commit")
    #         except cx_Oracle.DatabaseError as e:
    #             print(e)
    #     return {"res": file.filename}
