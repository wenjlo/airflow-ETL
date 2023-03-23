from datetime import datetime, timedelta
import yfinance as yf
import pendulum
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.models import Connection
from airflow.hooks.base import BaseHook

import json
from utils.sql import mysql_connector,write_batch_insert


def load_mysql():
    ip = 'host.docker.internal'
    db = 'mydatabase'
    user = 'chris'
    password = 'chris'
    query = """
        select * from stocks ;
    """
    data = mysql_connector(query, ip, db, user, password)
    print(data)

def write_sotck_to_mysql(**context):
    #stock_list = Variable.get("stock_list_json", deserialize_json=True)
    #stock_list = ["GE"]
    stock_list = ["IBM", "MSFT"]
    hook = BaseHook.get_connection("my_database")
    c = Connection(uri=hook.get_uri())
    # stocks = context["dag_run"].conf.get("stocks")
    # print(stocks)
    # if stocks:
    #     stock_list = stocks
    for ticker in stock_list:
        msft = yf.Ticker(ticker)
        hist = msft.history(period="1day")
        hist.insert(loc=0, column="stock_name", value=ticker)
        hist.insert(loc=0, column="date", value=hist.index)
        hist.columns = map(str.lower, hist.columns)
        hist = hist.rename(columns={"stock splits": "stock_splits"})
        write_batch_insert(df=hist, ip=c.host, user=c.login, password=c.password, table="stocks", db=c.schema)
        #write_batch_insert(df=hist, ip="host.docker.internal", user="chris", password="chris", table="stocks", db="mydatabase")
        print(f"Finished downloading {ticker} data.")
write_sotck_to_mysql()
with DAG(
        dag_id="sql_dags",
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),
        },
        # [END default_args]
        description='sql dag testing',
        schedule_interval=timedelta(days=1),
        start_date=pendulum.today('UTC').add(days=0),  # days_ago(2),
        catchup=False,
        tags=['chris_data'],
) as dag:
    load_sql = PythonOperator(
        task_id="write_to_mysql",
        python_callable=write_sotck_to_mysql,
        provide_context=True
    )
