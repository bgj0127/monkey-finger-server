from sqlalchemy import create_engine, select, insert, Table, MetaData
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv


def connDB(table):
  load_dotenv()
  try:
    engine = create_engine(f"postgresql://{os.getenv("USER")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{os.getenv("DB")}")
    metadata = MetaData()
    t = Table(table,metadata,autoload_with=engine)
    return engine, t
  except IntegrityError as e:
    print(f">>>>DB 연결 실패 {e}")



def initial_data(table,conn):
  d = {"wpm": [], "acc": [], "time": [], "mode": [], "mode2": [], "language": []}
  stmt = select(table.c.wpm, table.c.acc, table.c.timestamp, table.c.test_mode, table.c.test_mode2, table.c.language)
  result = conn.execute(stmt)
  for row in result:
    d["wpm"].append(row[0])
    d["acc"].append(row[1])
    d["time"].append(row[2])
    d["mode"].append(row[3])
    d["mode2"].append(row[4])
    d["language"].append(row[5])
  return d
