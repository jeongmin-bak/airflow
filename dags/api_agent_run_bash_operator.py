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
        env={'BS_DATE':'{{ (data_interval_end.in_timezone("Asia/Seoul") - macros.dateutil.relativedelta.relativedelta(months=1)) | ds}}'},
        
        bash_command= """
            /opt/airflow/plugins/shell/apiRunJob.sh RTMSDataSvcAptRent $BS_DATE
            echo "수집 기준일자 : $BS_DATE"
            """,
    )

    api_meta_run