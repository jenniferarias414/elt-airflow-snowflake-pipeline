# Airflow Snowflake Connection

## Purpose

This section validates that the Amazon MWAA Airflow environment can connect to Snowflake and execute SQL.

Before building the full pipeline DAG, a small test DAG is used to confirm the connection works.

```text
Airflow DAG
    ↓
Snowflake connection: snowflake_conn
    ↓
Snowflake SQL query
    ↓
Snowflake Query History validation
```

## Airflow Connection

The Airflow connection is created in the Airflow UI:

```text
Admin → Connections → Add Connection
```

Connection details:

| Field | Value |
|---|---|
| Connection ID | `snowflake_conn` |
| Connection Type | `Snowflake` |
| Schema | `BRONZE` |
| Warehouse | `COMPUTE_WH` |
| Database | `AIRFLOW_DB` |
| Role | `ACCOUNTADMIN` |

The Snowflake username, password, and account identifier are entered in the Airflow UI and are not stored in this repository.

## Test DAG

The test DAG is stored at:

```text
dags/test_snowflake_connection.py
```

It runs a simple Snowflake query:

```sql
SELECT CURRENT_TIMESTAMP AS AIRFLOW_SNOWFLAKE_TEST_TS;
```

## Why a Test DAG Is Useful

A small connection test is useful before building the full ELT DAG because it isolates one dependency:

```text
Can Airflow connect to Snowflake and execute SQL?
```

If this test succeeds, later pipeline errors are more likely related to pipeline SQL, staging, data files, or DAG task order rather than the base Snowflake connection.

## Validation

Validation is complete when:

- `test_snowflake_connection.py` is uploaded to the MWAA `dags/` folder.
- The DAG appears in the Airflow UI.
- The DAG run succeeds.
- The task logs show successful SQL execution.
- Snowflake Query History shows the test query.

## Screenshot Evidence

Recommended screenshots for this section:

```text
15-s3-test-snowflake-dag-uploaded.png
16-airflow-snowflake-connection-created.png
17-airflow-test-snowflake-dag-visible.png
18-airflow-test-snowflake-dag-success.png
19-airflow-test-snowflake-task-logs.png
20-snowflake-query-history-airflow-test.png
```
