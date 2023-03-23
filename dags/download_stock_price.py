#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.apache.org/tutorial.html)
"""
# [START tutorial]
# [START import_module]
from datetime import datetime, timedelta
import yfinance as yf
import pendulum
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from utils.sql import mysql_connector
import os
# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# [END import_module]


def download_price(**context):
    stock_list = Variable.get("stock_list_json", deserialize_json=True)
    stocks = context["dag_run"].conf.get("stocks")
    print(stocks)
    if stocks:
        stock_list = stocks
    for ticker in stock_list:
        msft = yf.Ticker(ticker)
        hist = msft.history(period="max")
        hist.to_csv(f'./logs/{ticker}.csv', index=False)
        print(f"Finished downloading {ticker} data.")
# [START instantiate_dag]
with DAG(
        dag_id="download_stock",
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),
        },
        # [END default_args]
        description='download stock',
        schedule_interval=timedelta(minutes=5),
        start_date=pendulum.today('UTC').add(days=-2),  # days_ago(2),
        catchup=False,
        tags=['chris_data'],
) as dag:
    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    download_task = PythonOperator(
        task_id="download_price",
        python_callable=download_price,
        provide_context=True
    )

    # [END documentation]

# [END tutorial]
