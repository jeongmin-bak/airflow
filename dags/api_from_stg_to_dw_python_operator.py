import pendulum
from airflow.sdk import DAG 
from airflow.providers.standard.operators.python import PythonOperator

with DAG(
    dag_id='api_from_stg_to_dw_python_operator',
    start_date=pendulum.datetime(2026, 4, 10, tz='Asia/Seoul'),
    schedule=None,
    catchup=False
) as dag:
    def insert_api_rent_data(oracle_conn_id, **kwargs):
        from airflow.providers.oracle.hooks.oracle import OracleHook
        from contextlib import closing

        oracle_hook = OracleHook(oracle_conn_id)
        with closing(oracle_hook.get_conn()) as conn:
            with closing(conn.cursor()) as cursor:
                dag_id = kwargs.get('ti').dag_id
                task_id = kwargs.get('ti').task_id
                run_id = kwargs.get('ti').run_id
                msg = 'hook insrt 수행'
                sql = """
                    INSERT INTO STG_APT_RENT_TSC
                            SELECT
                                jt.SGGCD,
                                jt.UMDNM,
                                jt.APTNM,
                                jt.JIBUN,
                                jt.EXCLUUSEAR,
                                jt.DEALYEAR,
                                jt.DEALMONTH,
                                jt.DEALDAY,
                                TO_NUMBER(REPLACE(jt.DEPOSIT, ',', '')) AS DEPOSIT,
                                jt.MONTHLYRENT,
                                jt.FLOOR,
                                jt.BUILDYEAR,
                                jt.CONTRACTTERM,
                                jt.CONTRACTTYPE,
                                jt.USERRRIGHT,
                                TO_NUMBER(REPLACE(jt.PREDEPOSIT, ',', '')) AS PREDEPOSIT,
                                jt.PREMONTHLYRENT,
                                jt.ROADNM,
                                jt.ROADNMSGGCD,
                                jt.ROADNMCD,
                                jt.ROADNMSEQ,
                                jt.ROADNMBCD,
                                jt.ROADNMBONBUN,
                                jt.ROADNMBUBUN,
                                jt.APTSEQ,
                                jt.DEALYEAR || LPAD(jt.DEALMONTH, 2, '0') AS BS_DT,
                                TO_CHAR(SYSDATE, 'YYYYMMDD') AS LOAD_DT
                            FROM STG_API_PARSED t,
                                JSON_TABLE(
                                        t.API_RSP_CN,
                                        '$'
                                        COLUMNS (
                                            SGGCD             VARCHAR2(5)      PATH '$.SGGCD',
                                            UMDNM             VARCHAR2(50)     PATH '$.UMDNM',
                                            APTNM             VARCHAR2(100)    PATH '$.APTNM',
                                            JIBUN             VARCHAR2(20)     PATH '$.JIBUN',
                                            EXCLUUSEAR        NUMBER           PATH '$.EXCLUUSEAR',
                                            DEALYEAR          NUMBER           PATH '$.DEALYEAR',
                                            DEALMONTH         NUMBER           PATH '$.DEALMONTH',
                                            DEALDAY           NUMBER           PATH '$.DEALDAY',
                                            DEPOSIT           VARCHAR2(20)     PATH '$.DEPOSIT',
                                            MONTHLYRENT       NUMBER           PATH '$.MONTHLYRENT',
                                            FLOOR             NUMBER           PATH '$.FLOOR',
                                            BUILDYEAR         NUMBER           PATH '$.BUILDYEAR',
                                            CONTRACTTERM      VARCHAR2(12)     PATH '$.CONTRACTTERM',
                                            CONTRACTTYPE      VARCHAR2(4)      PATH '$.CONTRACTTYPE',
                                            USERRRIGHT        VARCHAR2(4)      PATH '$.USERRRIGHT',
                                            PREDEPOSIT        VARCHAR2(20)     PATH '$.PREDEPOSIT',
                                            PREMONTHLYRENT    NUMBER           PATH '$.PREMONTHLYRENT',
                                            ROADNM            VARCHAR2(200)    PATH '$.ROADNM',
                                            ROADNMSGGCD       VARCHAR2(10)     PATH '$.ROADNMSGGCD',
                                            ROADNMCD          VARCHAR2(7)      PATH '$.ROADNMCD',
                                            ROADNMSEQ         VARCHAR2(2)      PATH '$.RADNMSEQ',
                                            ROADNMBCD         VARCHAR2(2)      PATH '$.ROADNMBCD',
                                            ROADNMBONBUN      VARCHAR2(5)      PATH '$.ROADNMBONBUN',
                                            ROADNMBUBUN       VARCHAR2(5)      PATH '$.ROADNMBUBUN',
                                            APTSEQ            VARCHAR2(20)     PATH '$.APTSEQ'
                                            )
                                    ) jt
                            WHERE t.SV_NM = 'RTMSDataSvcAptRent'
                """
                cursor.execute(sql)
                conn.commit()

    insert_oracle_with_hook = PythonOperator(
        task_id='insert_oracle_with_hook',
        python_callable=insert_api_rent_data,
        op_kwargs={'oracle_conn_id':'conn-db-oracle-meta'}
    )

    insert_oracle_with_hook