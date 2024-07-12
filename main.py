from enum import Enum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import cx_Oracle

id_val = ""
pw_val = ""
dsn = ""

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


class TestModel(str, Enum):
    test = "test"
    abc = "abc"
    hello = "hello"


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/wpm")
def wpm():
    select_all_wpm = "select wpm from monkey_type"
    cur.execute(select_all_wpm)
    wpm_list = cur.fetchall()
    l = []
    for i in wpm_list:
        l.append(i[0])
    return l


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


@app.get("/models/{model_name}")
async def model(model_name: TestModel):
    if model_name is TestModel.abc:
        return {"model_name": model_name, "message": "test Model~"}


# dummy_db = [{"item:name": "Foo"}, {"item:name": "Bar"}, {"item:name": "Baz"}]


# @app.get("/items/")
# async def read_items(skip: int = 0, limit: int = 10):
#     return dummy_db[skip : skip + limit]


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
