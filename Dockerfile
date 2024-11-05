FROM apache/airflow:2.10.2
RUN pip3 install yfinance
RUN pip install pandas
