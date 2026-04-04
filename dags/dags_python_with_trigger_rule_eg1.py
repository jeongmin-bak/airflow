import pendulum

from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.exceptions import AirflowException
from airflow.sdk import DAG, task 

with DAG(
    dag_id='dags_branch_python_operator',
    schedule=None,
    start_date=pendulum.datetime(2023, 4, 1, tz='Asia/Seoul'),
    catchup=False
) as dag:
    bash_upstream_1 = BashOperator(
        task_id='bash_upstream_1',
        bash_command='echo upstream'
    )

    @task(task_id='python_upstream')
    def python_upstream_1():
        raise AirflowException('downstream_1 Exception!')
    
    @task(task_id='python_upstream_2')
    def python_upstream_2():
        print('정상처리')

    @task(task_id='python_downstream_1', trigger_rule='all_done')
    def python_downstream_1():
        print('정상처리')


    [bash_upstream_1, python_upstream_1(), python_upstream_2()] >> python_downstream_1()   