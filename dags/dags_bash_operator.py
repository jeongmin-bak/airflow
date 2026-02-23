from __future__ import annotations

import pendulum

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG, chain

with DAG(
    dag_id="dags_bash_operator",
    schedule=None,
    start_date=pendulum.datetime(2026, 2, 24, tz="Asia/Seoul"),
    catchup=False,
) as dag:
    bash_t1 = BashOperator(
        task_id="bash_t1",
        bash_command="echo whoami",
    )

    bash_t2 = BashOperator(
        task_id="bash_t2",
        bash_command="echo $HOSTNAME",
    )

    bash_t1 >> bash_t2