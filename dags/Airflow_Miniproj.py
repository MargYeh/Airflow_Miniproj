#%%
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import date, datetime, timedelta
import yfinance as yf
import pandas as pd
import os

def get_data_AAPL():
    start_date = date.today()
    end_date = start_date + timedelta(days=1)
    aapl_df = yf.download('AAPL', start=start_date, end=end_date, interval = '1m')
    aapl_df.to_csv('AAPL_data.csv', header=False)

def get_data_TSLA():
    start_date = date.today()
    end_date = start_date + timedelta(days=1)
    tsla_df = yf.download('TSLA', start=start_date, end=end_date, interval = '1m')
    tsla_df.to_csv('TSLA_data.csv', header=False)

def query_head(path):
    AAPL_df = pd.read_csv(f'{path}/AAPL_data.csv')
    print('Sample AAPL data')
    print(AAPL_df.head())

    TSLA_df = pd.read_csv(f'{path}/TSLA_data.csv')
    print('Sample TSLA data')
    print(TSLA_df.head())

# Creating the Airflow DAG
''' This DAG has the following configurations:
    Start time and date: 6 PM on current date
    Job interval: Runs once daily
    Only runs on weekdays (Monday - Friday)
    If failed: retry twice with a 5 minute interval
'''
default_args ={
    'owner': 'Margaret',
    'start_date': datetime.now().replace(hour=18, minute=0, second=0),
    'retries':2,
    'retry_delay':timedelta(minutes=5)
}
dag = DAG(
    'marketvol', 
    default_args=default_args, 
    description='A simple DAG', 
    schedule_interval='0 18 * * 1-5') #minutes, hours, day, month, days of the week

# Set up the BashOperator to make a directory with the name of the execution date
t0 = BashOperator(
    task_id = 'temp_dir',
    bash_command = 'mkdir -p /tmp/data/{{ds}}',
    dag=dag
)

#Create a PythonOperator to download market data
t1 = PythonOperator(
    task_id = 'get_data_AAPL',
    python_callable=get_data_AAPL,
    provide_context=True,
    dag=dag
)

t2 = PythonOperator(
    task_id = 'get_data_TSLA',
    python_callable=get_data_TSLA,
    provide_context=True,
    dag=dag
)

#Create a BashOperator to move the downloaded file to the created directory
#download_location = os.getcwd()

t3 = BashOperator(
    task_id = 'tmp_move_AAPL',
    bash_command = 'mv ./AAPL_data.csv /tmp/data/{{ds}}/',
    dag=dag
)

t4 = BashOperator(
    task_id = 'tmp_move_TSLA',
    bash_command = 'mv ./TSLA_data.csv /tmp/data/{{ds}}/',
    dag=dag
)

#Run a query on the files

t5 = PythonOperator(
    task_id = 'query',
    python_callable=query_head,
    dag=dag,
    op_kwargs={'path':'/tmp/data/{{ds}}'}
)

t0 >> [t1, t2]
t1 >> t3
t2 >> t4
[t3, t4] >> t5

