import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG, task 

with DAG(
    dag_id='dags_bash_python_with_xcom_2',
    schedule='30 9 * * *',
    start_date=pendulum.datetime(2023, 4, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    @task(task_id='python_push')
    def python_push_xcom():
        result_dict = {'status':'Good','data':[1,2,3],'options_cnt':100}
        return result_dict 
    
    bash_pull = BashOperator(
        task_id='bash_pull',
        env={
            'STATUS': '{{ti.xcom_pull(task_ids="python_push")["status"]}}',
            'DATA': '{{ti.xcom_pull(task_ids="python_push")["status"]}}',
            "OPTIONS_CNT": '{{ti.xcom_pull(task_ids="python_push")["options_cnt"]}}'
        },
        bash_command='echo $STATUS && echo $DATA && echo $OPTIONS_CNT'
    )

    python_push_xcom() >> bash_pull

    bash_push = BashOperator(
        task_id='bash_push',
        bash_command='echo PUSH_START '
                    '{{ti.xcom_push(key="bash_pushed", value=200)}} &&'
                    'echo PUSH_COMPLETE'
    )

    @task
    def python_pull_xcom(**kwargs):
        ti = kwargs['ti']
        status_value = ti.xcom_pull(key='bash_pushed', task_ids='bash_push')
        return_value = ti.xcom_pull(key='bash_push')
        print('status_value: ' + str(status_value))
        print('return_value: ' + str(return_value))

    bash_push >> python_pull_xcom()
