FROM apache/airflow:2.10.2
RUN pip install yfinance
RUN pip install pandas
