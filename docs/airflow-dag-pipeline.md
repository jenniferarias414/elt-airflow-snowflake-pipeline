# Airflow DAG Setup and Pipeline Validation

## Purpose

This section creates and validates the full healthcare ELT pipeline DAG.

The DAG coordinates extraction from a public GitHub CSV source, uploads files to Amazon S3, loads raw data into Snowflake Bronze tables, runs Silver transformation stored procedures, and runs Gold aggregation stored procedures.

```text
GitHub CSV files
      ↓
Airflow Python task
      ↓
Amazon S3 raw/
      ↓
Snowflake Bronze COPY INTO
      ↓
Snowflake Silver stored procedures
      ↓
Snowflake Gold stored procedures
```

## DAG Created

| DAG | Purpose |
|---|---|
| `healthcare_elt_pipeline` | Orchestrates the full ELT pipeline from source files to Snowflake Gold tables |

## DAG Task Groups

### 1. Extract and Upload

The Python task downloads CSV files from the GitHub source and uploads them to the project S3 data bucket under the `raw/` prefix.

### 2. Bronze Loads

Five Snowflake SQL tasks truncate and reload the Bronze raw tables using `COPY INTO`.

Bronze tables loaded:

- `DOCTORS_RAW`
- `HOSPITALS_RAW`
- `PATIENTS_RAW`
- `TREATMENTS_RAW`
- `VISITS_RAW`

### 3. Silver Transformations

Three Snowflake stored procedure calls create transformed Silver tables:

- `PATIENTS_TRANSFORM`
- `TREATMENTS_TRANSFORM`
- `VISITS_TRANSFORM`

### 4. Gold Aggregations

Four Snowflake stored procedure calls create analytics-ready Gold aggregate tables:

- `CITY_HEALTHCARE_ACCESS_AGG`
- `HOSPITAL_PERFORMANCE_AGG`
- `PATIENT_VALUE_AGG`
- `PATIENT_VISIT_SUMMARY_AGG`

## Implementation Notes

The DAG uploads source CSV files to the `raw/` prefix instead of the S3 bucket root.

This keeps incoming files organized and aligns with the project data bucket structure:

```text
raw/       incoming source files
staged/    files prepared for loading or future processing
archive/   optional processed-file storage
```

The Snowflake stage points to the data bucket, and the DAG references files under the `raw/` prefix during the Bronze `COPY INTO` steps.

## Validation

The pipeline is validated when:

- the DAG appears in Airflow
- the DAG run succeeds
- files are uploaded to S3 under `raw/`
- Bronze tables contain data
- Silver transform tables contain data
- Gold aggregate tables contain data

The primary validation query is stored at:

```text
snowflake/sql/06_validate_pipeline_outputs.sql
```

## Screenshot Evidence

Recommended final screenshots:

```text
21-airflow-healthcare-dag-visible.png
22-airflow-healthcare-dag-success.png
23-snowflake-pipeline-row-count-validation.png
```
