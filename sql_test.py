import mysql.connector
from mysql.connector import Error

# connection = mysql.connector.connect(
#         host='127.0.0.1',          # 主機名稱
#         database='mydatabase', # 資料庫名稱
#         user='chris',        # 帳號
#         password='chris')  # 密碼

import asyncio
import aiomysql
import pandas as pd


def mysql_connector(query, ip, db, user, password):
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host=ip,
            database=db,
            user=user,
            password=password)

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            record = cursor.fetchall()
            columns = cursor.column_names
    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    print(f" normal result : {list(record)}")
    return pd.DataFrame.from_records(list(record), columns=columns)


def load_mysql():
    ip = '127.0.0.1'
    db = 'mydatabase'
    user = 'chris'
    password = 'chris'
    query = """
        select * from stocks ;
    """
    data = mysql_connector(query, ip, db, user, password)
    data.to_csv("./df2.csv", index=False)


load_mysql()


async def basic_test():
    conn = await aiomysql.connect(host="127.0.0.1", port=3306,
                                  user='chris', password='chris',
                                  db='mydatabase', charset='utf8')
    cursor = await conn.cursor()
    await cursor.execute('select * from stocks')
    result = await cursor.fetchall()
    print(f" async result : {list(result)}")
    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame.from_records(list(result), columns=columns)
    # for record in result:
    #     print("record: ",record )
    df.to_csv('./df.csv', index=False)
    await cursor.close()
    conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(basic_test())
