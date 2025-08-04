from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from etl_pipeline import extract_data, transform_data, load_data

default_args = {
    'owner': 'lethabo',
    'start_date': datetime(2025, 8, 1),
    'retries': 1,
}

with DAG(
    dag_id='csv_to_sql_etl',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['etl', 'postgres', 'csv']
) as dag:

    def extract_task(**context):
        df = extract_data()
        context['ti'].xcom_push(key='raw_df', value=df.to_json())
    
    def transform_task(**context):
        import pandas as pd
        raw_json = context['ti'].xcom_pull(key='raw_df', task_ids='extract')
        df = pd.read_json(raw_json)
        transformed = transform_data(df)
        context['ti'].xcom_push(key='clean_df', value=transformed.to_json())

    def load_task(**context):
        import pandas as pd
        clean_json = context['ti'].xcom_pull(key='clean_df', task_ids='transform')
        df = pd.read_json(clean_json)
        load_data(df)

    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_task,
        provide_context=True
    )

    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_task,
        provide_context=True
    )

    load = PythonOperator(
        task_id='load',
        python_callable=load_task,
        provide_context=True
    )

    extract >> transform >> load
