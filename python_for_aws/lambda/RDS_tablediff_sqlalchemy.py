# pip install  sqlalchemy , mysql-connector-python
from sqlalchemy import create_engine , text




e1 = create_engine("mysql+mysqlconnector://root:ooVsRCalC5&U1@localhost:3306/test")
e2 = create_engine("mysql+mysqlconnector://root:ooVsRCalC5&U1@localhost:3306/test")

# def diff(a, b):
#     a = [tuple(sorted(d.items())) for d in a]
#     b = [tuple(sorted(d.items())) for d in b]
#     return [dict(kvs) for kvs in set(a).difference(b)]


# connect to the database
d1 = e1.connect()
d2 = e2.connect()


tables = d1.execute(text("show tables"))

for i in tables:
    table = i[0]
    li1 = d1.execute(text(f'select * from {table}')).fetchall()
    li2 = d2.execute(text(f'select * from {table}')).fetchall()
    t1 = set(li1)
    t2 = set(li2)
    diff1 = t1 - t2
    diff2 = t2 - t1
    print(f"first db {table} ")
    print(diff1)
    print(f"second db {table} ")
    print(diff2)

