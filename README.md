# ELT Data Pipeline with Airflow and Snowflake

This project builds and validates an ELT data pipeline using Amazon S3, Snowflake, and Amazon Managed Workflows for Apache Airflow.

The pipeline extracts healthcare CSV files from a public GitHub source, lands the files in S3, loads raw data into Snowflake Bronze tables, transforms the data into Silver tables, and creates Gold aggregate tables for analytics-style reporting.

## Architecture

```text
GitHub Healthcare CSV Source
        ↓
Airflow Python Task
        ↓
Amazon S3 raw/ landing area
        ↓
Snowflake Bronze raw tables
        ↓
Snowflake Silver transformation stored procedures
        ↓
Snowflake Gold aggregation stored procedures
```

## What This Project Demonstrates

This project demonstrates how several cloud data engineering services work together in an ELT workflow:

| Component | Role in the Pipeline |
|---|---|
| Apache Airflow / MWAA | Orchestrates the workflow and controls task order |
| PythonOperator | Downloads source files and uploads them to S3 |
| Amazon S3 | Stores source CSV files before Snowflake loads them |
| Snowflake Storage Integration | Allows Snowflake to securely access S3 |
| Snowflake External Stage | Points Snowflake to the S3 data location |
| Snowflake Bronze Layer | Stores raw source data |
| Snowflake Silver Layer | Cleans, joins, and standardizes data |
| Snowflake Gold Layer | Creates analytics-ready aggregate tables |
| IAM Roles and Policies | Control AWS access for Snowflake and Airflow |

## Data Flow

The pipeline follows an ELT pattern:

```text
Extract → Load → Transform
```

1. Airflow runs a Python task that downloads CSV files from GitHub.
2. The files are uploaded to the project S3 data bucket under `raw/`.
3. Snowflake loads the CSV files into Bronze raw tables using `COPY INTO`.
4. Snowflake stored procedures transform Bronze data into Silver tables.
5. Snowflake stored procedures aggregate Silver data into Gold tables.
6. Final validation queries confirm row counts across Bronze, Silver, and Gold.

## Snowflake Layer Design

### Bronze

The Bronze layer stores raw data from the source files. Columns are stored as strings to keep ingestion flexible.

Bronze tables:

- `DOCTORS_RAW`
- `HOSPITALS_RAW`
- `PATIENTS_RAW`
- `TREATMENTS_RAW`
- `VISITS_RAW`

### Silver

The Silver layer applies transformations such as type conversion, name parsing, joins, and standardization.

Silver tables created by stored procedures:

- `PATIENTS_TRANSFORM`
- `TREATMENTS_TRANSFORM`
- `VISITS_TRANSFORM`

### Gold

The Gold layer contains analytics-ready aggregate tables.

Gold tables created by stored procedures:

- `CITY_HEALTHCARE_ACCESS_AGG`
- `HOSPITAL_PERFORMANCE_AGG`
- `PATIENT_VALUE_AGG`
- `PATIENT_VISIT_SUMMARY_AGG`

## Key Implementation Choices

- S3 files are organized under `raw/` instead of being placed at the bucket root.
- Snowflake accesses S3 through a storage integration and IAM role rather than raw AWS keys.
- IAM permissions are scoped to project buckets instead of using broad S3 access.
- Airflow stores connection details in the Airflow UI connection manager, not in DAG code.
- Snowflake stored procedures hold transformation logic while Airflow handles orchestration.

## Repository Structure

```text
.
├── airflow/
│   └── requirements.txt
├── aws/
│   └── iam/
├── dags/
│   ├── healthcare_elt_pipeline.py
│   └── test_snowflake_connection.py
├── docs/
├── learning-notes/
├── screenshots/
├── snowflake/
│   └── sql/
└── notes/private/        # gitignored private build notes
```

## Validation

The project was validated through:

- successful Snowflake storage integration setup
- successful Snowflake external stage access
- successful Airflow-to-Snowflake test DAG
- successful full healthcare ELT DAG run
- S3 files uploaded under the `raw/` prefix
- Snowflake row-count validation across Bronze, Silver, and Gold tables

The final validation SQL is stored at:

```text
snowflake/sql/06_validate_pipeline_outputs.sql
```

## Important Screenshots

This project captured screenshots throughout the build. The most important proof points are:

| Screenshot | Evidence |
|---|---|
| `08-snowflake-external-stage-list-success.png` | Snowflake can access the S3 stage |
| `18-airflow-test-snowflake-dag-success.png` | Airflow can connect to Snowflake |
| `22-airflow-healthcare-dag-success.png` | Full ELT DAG completed successfully |
| `23-snowflake-pipeline-row-count-validation.png` | Bronze, Silver, and Gold tables contain data |

## Cost Control

This project uses AWS resources that should be reviewed and cleaned up after validation, especially the MWAA environment.

Cleanup targets include:

- MWAA environment
- MWAA CloudFormation networking stack
- S3 buckets and objects
- IAM roles and inline policies
- CloudWatch log groups
- Snowflake database objects, if no longer needed

## Project Status

Completed and validated:

- AWS IAM role for Snowflake S3 access
- S3 buckets for Airflow files and pipeline data
- Snowflake storage integration and external stage
- Bronze raw tables
- Silver transformation stored procedures
- Gold aggregation stored procedures
- MWAA environment
- Airflow Snowflake connection
- test DAG
- full healthcare ELT DAG
- final Snowflake output validation
