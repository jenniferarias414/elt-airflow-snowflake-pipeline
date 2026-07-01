# Managed Apache Airflow Environment

## Purpose

This section creates an Amazon Managed Workflows for Apache Airflow environment for orchestrating the ELT pipeline.

Airflow is responsible for coordinating pipeline tasks. In this project, Snowflake performs the data transformations and Airflow controls when those transformations run.

```text
Airflow DAG
    ↓
S3 staging/load steps
    ↓
Snowflake stored procedures
    ↓
Bronze → Silver → Gold workflow
```

## Environment Created

| Resource | Value |
|---|---|
| MWAA environment | `jenny-elt-airflow` |
| DAG source bucket | `jennyarias-elt-airflow-files` |
| DAG folder | `dags/` |
| Requirements file | `requirements.txt` |
| Environment class | `mw1.micro` |
| Web server access | Public network for lab access |

## Requirements File

The Airflow requirements file includes:

```text
apache-airflow-providers-snowflake
snowflake-connector-python
```

These packages allow Airflow to connect to Snowflake and use Snowflake-related operators/hooks.

## Implementation Notes

The Airflow files bucket is separate from the pipeline data bucket.

```text
jennyarias-elt-airflow-files = DAGs and requirements
jennyarias-elt-airflow-data  = data files for Snowflake loading
```

This keeps orchestration files separate from data files and makes the project easier to troubleshoot.

## IAM Permission Choice

Instead of attaching broad S3 access to the MWAA execution role, this project uses a scoped inline policy for the project buckets.

The execution role receives:

- read access to the Airflow files bucket
- read/write access to the project data bucket
- list access to both project buckets

This keeps the role focused on the resources used by this pipeline.

## Cost Control

MWAA can create ongoing charges while the environment exists.

The environment should be deleted after the project is validated and screenshots are captured.
