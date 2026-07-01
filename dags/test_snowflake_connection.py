from datetime import datetime

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


DEFAULT_ARGS = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 0,
}


with DAG(
    dag_id="test_snowflake_connection",
    default_args=DEFAULT_ARGS,
    schedule=None,
    catchup=False,
    description="Test DAG to validate the Airflow Snowflake connection",
    tags=["test", "snowflake"],
) as dag:

    run_test_query = SQLExecuteQueryOperator(
        task_id="run_test_query",
        conn_id="snowflake_conn",
        sql="""
            USE WAREHOUSE COMPUTE_WH;
            USE DATABASE AIRFLOW_DB;
            USE SCHEMA BRONZE;
            SELECT CURRENT_TIMESTAMP AS AIRFLOW_SNOWFLAKE_TEST_TS;
        """,
    )
