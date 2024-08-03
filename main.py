from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Path
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from DB_Control import connDB, filtered_data

engine, table = connDB("MONKEY_FINGER")

app = FastAPI()

origins = ["http://localhost:5173/", "https://monkeyfinger.netlify.app"]
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
    print(lanFilter, modeFilter)
    with engine.connect() as conn:
        try:
            return filtered_data(table, conn, lanFilter, modeFilter)
        except HTTPException as e:
            print(e)
            return {"data": {"None"}, "status": e.status_code}
    # return {"language": filter_type.language, "mode": filter_type.mode}

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
