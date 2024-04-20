# pip install pandas , sqlalchemy , mysql-connector-python
from sqlalchemy import create_engine , text
import pandas as pd



e1 = create_engine("mysql+mysqlconnector://root:ooVsRCalC5&U1@localhost:3306/employees")
e2 = create_engine("mysql+mysqlconnector://root:ooVsRCalC5&U1@localhost:3306/employees")

# connect to the database
d1 = e1.connect()
d2 = e2.connect()

# check diff in tables
def check_diif(t1 , t2 , engine1 , engine2):
    query_table1 = f'SELECT * FROM {t1}'
    query_table2 = f'SELECT * FROM {t2}'
    table1_df = pd.read_sql(query_table1, engine1)
    table2_df = pd.read_sql(query_table2, engine2)
    comparison_df = table1_df.merge(table2_df, indicator=True, how='outer')
    diff_df = comparison_df[comparison_df['_merge'] != 'both']
    # return true when there is no difference
    return diff_df 
    


# get the list of tables
tables = d1.execute("show tables")

for i in tables:
    table = i[0]
    diff = check_diif(table , table , d1 , d2)
    if diff.empty:
        print(f"Table {table} is the same")
    else:
        print(f"Table {table} is not the same")
        print(diff)
        # return 
        print( diff.to_html())
