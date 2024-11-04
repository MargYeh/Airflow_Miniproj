# Airflow_Miniproj

## Description
This project uses Airflow to download data from Yahoo Finance on a schedule and stores the data into a single directory. It uses BashOperator and PythonOperator to run queries to show the first five lines of downloaded data.

## Setup Instructions
- Run using the following command

```docker compose build && docker compose up -d```

You should see the following text in the command line on a successful run:

![image](https://github.com/user-attachments/assets/1bc1af5c-a658-42cb-8c17-f1a0badff15b)

- Log in at localhost:8080 using the user/pass 'airflow'

- Toggle the DAG to schedule the run as shown below
  
![image](https://github.com/user-attachments/assets/370776bb-9955-4e2e-9644-37aea91d6c6e)

- Examining the DAG should show the following layout:
  
![image](https://github.com/user-attachments/assets/b239fbe7-d143-4559-9fed-e8553ef6f37e)

