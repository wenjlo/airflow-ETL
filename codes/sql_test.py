import mysql.connector
import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(
        host='127.0.0.1',          # 主機名稱
        database='mydatabase', # 資料庫名稱
        user='chris',        # 帳號
        password='chris')  # 密碼

