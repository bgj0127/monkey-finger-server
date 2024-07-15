from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import cx_Oracle

id_val = "HR"
pw_val = "12345"
dsn = "localhost:1521/XE"

conn = cx_Oracle.connect(id_val, pw_val, dsn)
cur = conn.cursor()
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/default")
def default():
    select_all_wpm = "select wpm, acc, timestamp from monkey_type order by timestamp"
    cur.execute(select_all_wpm)
    wpm_list = cur.fetchall()
    d = {"wpm": [], "acc": [], "time": []}
    for i in wpm_list:
        d["wpm"].append(i[0])
        d["acc"].append(i[1])
        d["time"].append(i[2])
    return d


# @app.get("/")
# def info():
#     filtering = ""
#     cur.execute(filtering)
#     data = cur.fetchall()

#     return ""

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}


# @app.get("/users/{user_id}/items/{item_id}")
# async def user_item(user_id: int, item_id: str, short: bool = False):
#     item = {"owner_id": user_id, "item_id": item_id}
#     if not short:
#         item.update({"description": "긴 문장 어쩌고 저쩌고"})
#     return item
