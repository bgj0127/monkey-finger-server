import cx_Oracle

id_val = "HR"
pw_val = "12345"
dsn = "localhost:1521/XE"

conn = cx_Oracle.connect(id_val, pw_val, dsn)
cur = conn.cursor()
