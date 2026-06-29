# Bronze Layer Objects

## Purpose

The Bronze layer stores raw source data structures in Snowflake.

In this project, the Bronze schema contains raw tables for healthcare-related entities:

- doctors
- hospitals
- patients
- visits
- treatments

The Bronze layer is intentionally close to the source format. Data cleanup, type casting, joining, and business logic will be handled in later layers.

## Objects Created

| Table | Purpose |
|---|---|
| `DOCTORS_RAW` | Raw doctor reference data |
| `HOSPITALS_RAW` | Raw hospital reference data |
| `PATIENTS_RAW` | Raw patient reference data |
| `VISITS_RAW` | Raw visit/event data |
| `TREATMENTS_RAW` | Raw treatment details linked to visits |

## Why the Columns Are Strings

The Bronze tables use `STRING` columns because this layer is designed for raw ingestion.

This keeps the initial load flexible and avoids failing early because of source formatting issues. For example, dates and costs may arrive as text first and then be converted to proper data types in the Silver layer.

```text
Bronze = land the data first
Silver = clean and standardize
Gold = curate for analytics
```

## Validation

Validation is complete when all five raw tables exist in:

```text
AIRFLOW_DB.BRONZE
```

The validation query used is:

```sql
SHOW TABLES IN SCHEMA AIRFLOW_DB.BRONZE;
```
