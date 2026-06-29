# S3 Buckets for Airflow and Snowflake

## Purpose

This project uses two S3 buckets:

| Bucket | Purpose |
|---|---|
| `jennyarias-elt-airflow-files` | Stores Airflow DAG files and MWAA requirements |
| `jennyarias-elt-airflow-data` | Stores pipeline data files that Snowflake will load |

## Airflow Files Bucket

The Airflow files bucket contains:

```text
dags/
requirements.txt
```

The `dags/` prefix is where Airflow DAG files will be uploaded later.

The `requirements.txt` file contains Python packages that the managed Airflow environment needs to install.

Current requirements:

```text
apache-airflow-providers-snowflake
snowflake-connector-python
```

## Data Bucket

The data bucket is used as the landing and staging area for pipeline data.

The project creates these prefixes:

```text
raw/
staged/
archive/
```

These prefixes make the data flow easier to understand and separate incoming files from files that are ready for loading or archival.

## Security Configuration

Public access is blocked on both buckets.

For the Snowflake IAM role, this project uses a bucket-scoped policy instead of broad `AmazonS3FullAccess`.

The role is allowed to read from the project data bucket only.

## Validation

Validation includes confirming that:

- both buckets exist
- `dags/` exists in the Airflow files bucket
- `requirements.txt` exists in the Airflow files bucket
- data prefixes exist in the data bucket
- the Snowflake IAM role has a bucket-scoped S3 policy attached
