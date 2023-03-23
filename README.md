# airflow-ETL
   - airflow 在 docker 建置部署

# 1. Build DockerFile
##### 我們預先安裝 python 會用到的套件
##### 在 Dockerfile 中引入requirements.txt 的pip install 
----------------------------------------------------------------
    Dockerfile:
    FROM apache/airflow:latest
    COPY requirements.txt .
    RUN pip install --user --upgrade pip
    RUN pip install --no-cache-dir --user -r requirements.txt
# 2. Build new Airflow image
    In same folder run:
    docker build . --tag pyrequire_airflow:2.3.3 
    or
    docker build . --tag <your_image_name>:version 

# 3. Setting docker-compose.yml
[docker-compose.yml](https://airflow.apache.org/docs/apache-airflow/2.5.2/docker-compose.yaml)
# 4. Running docker(first time)
     docker compose up airflow-init
