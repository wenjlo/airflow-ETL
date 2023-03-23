from sqlalchemy import create_engine
import mysql.connector
from mysql.connector import Error
import pandas as pd
import pymysql


def connect_mysql(ip, user, password, query, db, out_columns):
    conn = pymysql.connect(host=ip, port=3306, user=user, password=password, db=db, charset='utf8')
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    data = pd.DataFrame.from_records(list(rows), columns=out_columns)
    conn.close()
    return data


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

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

    return pd.DataFrame.from_records(list(record), columns=cursor.column_names)


def read_sql_from_query(sql_ip, port, user, password, db, query):
    conn = pymysql.connect(sql_ip, port=port, user=user, passwd=password, db=db)
    return pd.read_sql(query, conn)


def pd_tosql(sql_ip, user, password, database, df, table_name):
    engine = create_engine(
        "mysql+pymysql://{account}:{passowrd}@{IP}:3306/{database}".format(IP=sql_ip, account=user, passowrd=password,
                                                                           database=database))

    df.to_sql(table_name, if_exists='fail', con=engine, index=False)


def read_sql_from_query(sql_ip, port, user, password, db, query):
    conn = pymysql.connect(sql_ip, port=port, user=user, passwd=password, db=db)
    return pd.read_sql(query, conn)


def pd_tosql(sql_ip, user, password, database, df, table_name):
    engine = create_engine(
        "mysql+pymysql://{account}:{passowrd}@{IP}:3306/{database}".format(IP=sql_ip, account=user, passowrd=password,
                                                                           database=database))

    df.to_sql(table_name, if_exists='fail', con=engine, index=False)


def gen_data_from_batch(df, batch=256):
    values = []
    n = df.shape[0]

    if n % batch != 0:
        n_batch = n // batch
    else:
        n_batch = n // batch - 1

    for i in range(n_batch + 1):
        if i < n_batch:
            start = i * batch
            end = i * batch + batch
        else:

            start = i * batch
            end = n

        yield df.iloc[start:end, :]


def gen_recode_to_insert(df):
    records_to_insert = []
    for i in df.values.tolist():
        records_to_insert.append(tuple(i))
    return records_to_insert


def batch_insert(records, conn, table, n_col):
    query = "insert ignore into " + table + " values (" + ",".join(["%s"] * n_col) + ")"
    # query = "insert into "+table+" values (" + ",".join(["%s"]*n_col)+")"
    cur = conn.cursor()

    cur.executemany(query, records)
    # cur.close()
    conn.commit()


def write_batch_insert(df, ip, user, password, table, db):
    conn = pymysql.connect(host=ip, port=3306, user=user, password=password, db=db, charset='utf8')
    n_col = len(df.columns)
    for i in gen_data_from_batch(df):
        rec = gen_recode_to_insert(i)
        batch_insert(rec, conn, table, n_col)
    conn.close()
