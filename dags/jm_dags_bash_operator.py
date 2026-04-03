import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG, chain

with DAG(
    dag_id="dags_bash_operator",
    schedule=None,
    start_date=pendulum.datetime(2026, 3, 12, tz="Asial/Seoul"),
) as dag:
    bash_t1 = BashOperator(
        
    )