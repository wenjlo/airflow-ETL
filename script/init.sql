CREATE DATABASE IF NOT EXISTS metastore;
CREATE USER 'localuser'@'localhost' IDENTIFIED BY 'airflow';
GRANT ALL PRIVILEGES ON metastore . * TO 'root'@'localhost';
FLUSH PRIVILEGES;