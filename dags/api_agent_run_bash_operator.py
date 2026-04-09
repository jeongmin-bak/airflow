import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG(
    dag_id="api_agent_run_bash_operator",
    schedule="10 0 1 * 6#1",
    start_date=pendulum.datetime(2026, 4, 9, tz="Asia/Seoul"),
    catchup=False
) as dag:
    
    api_meta_run = BashOperator(
        task_id="api_meta_run",
        bash_command="/opt/airflow/plugins/shell/apiRunJob.sh 1234 20250409",
    )

    api_meta_run