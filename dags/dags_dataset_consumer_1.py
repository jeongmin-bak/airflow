import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG
from airflow.datasets import Dataset

dataset_dags_dataset_producer_1 = Dataset("dags_dataset_producer_1")

with DAG(
        dag_id='dags_dataset_producer_1',
        schedule=[dataset_dags_dataset_producer_1],
        start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
        catchup=False,
        tags=['asset','producer']
) as dag:
    bash_task = BashOperator(
        task_id = 'bash_task',
        bash_command='echo {{ ti.run_id }} && echo "producer_1 이 완료되면 수행"'
    )