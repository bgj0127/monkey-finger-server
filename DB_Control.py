from sqlalchemy import create_engine, select, desc, asc, Table, MetaData, or_, text
from sqlalchemy.exc import IntegrityError, DatabaseError
from sqlalchemy_views import CreateView
import os
from dotenv import load_dotenv


def connDB(table):
    load_dotenv()
    try:
        engine = create_engine(
            f"postgresql://{os.getenv("USER")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{os.getenv("DB")}")
        metadata = MetaData()
        t = Table(table, metadata, autoload_with=engine)
        return engine, t, metadata
    except IntegrityError as e:
        print(f">>>>DB 연결 실패 {e}")

def filtered_data(table, conn, lan: list, mode: list):
    view = Table('MONKEY_FINGER_VIEW', MetaData())
    lan_l = []
    mode_l = []
    for s in lan:
        lan_l.append(f"'{s}%'")
    for s in mode:
        mode_l.append(f"'{s}'")
    d = {"wpm": [], "acc": [], "time": [],
         "mode": [], "mode2": [], "language": [], "duration": []}
    result = []
    stmt = select(table.c.wpm, table.c.acc, table.c.timestamp,
                    table.c.test_mode, table.c.test_mode2, table.c.language, table.c.test_duration).where(
        or_(*[table.c.language.like(pattern) for pattern in lan_l])
    ).where(table.c.test_mode.in_(mode_l)).order_by(asc(table.c.timestamp))
    try:
        create_view = CreateView(view,stmt,or_replace=True)
        cv = str(create_view.compile())
        try:
            conn.execute(text(cv))
            conn.commit()
        except DatabaseError as e:
            print("execute text 에러",e)
        
        result = conn.execute(stmt).all()
    except DatabaseError as e:
        print(e)

    for row in result:
        d["wpm"].append(row[0])
        d["acc"].append(row[1])
        d["time"].append(row[2])
        d["mode"].append(row[3])
        d["mode2"].append(row[4])
        d["language"].append(row[5])
        d['duration'].append(row[6])
    return d

def view(table, conn):
    stmt = select(table.c.wpm, table.c.acc, table.c.test_duration)
    result = str(conn.execute(stmt).all()).strip()
    return result
