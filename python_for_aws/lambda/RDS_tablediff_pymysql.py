# pip install pymysql
import pymysql.cursors


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='ooVsRCalC5&U1',
                             database='test',
                             cursorclass=pymysql.cursors.DictCursor)

connection2 = pymysql.connect(host='localhost',
                             user='root',
                             password='ooVsRCalC5&U1',
                             database='test',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * from t1"
        cursor.execute(sql)
        d1 = cursor.fetchall()

with connection2:
    with connection2.cursor() as cursor:
        # Read a single record
        sql = "SELECT * from t2"
        cursor.execute(sql)
        d2 = cursor.fetchall()

def diff(a, b):
    a = [tuple(sorted(d.items())) for d in a]
    b = [tuple(sorted(d.items())) for d in b]
    return [dict(kvs) for kvs in set(a).difference(b)]