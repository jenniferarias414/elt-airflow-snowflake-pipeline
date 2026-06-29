# Silver Layer Objects

## Purpose

The Silver layer contains transformation logic that cleans, standardizes, and joins raw Bronze data into more usable tables.

In this project, the Silver layer is created through Snowflake stored procedures.

## Stored Procedures Created

| Stored Procedure | Creates Table | Purpose |
|---|---|---|
| `PATIENTS_TRANSFORM_SP` | `PATIENTS_TRANSFORM` | Cleans and standardizes patient data |
| `TREATMENTS_TRANSFORM_SP` | `TREATMENTS_TRANSFORM` | Combines treatment, visit, patient, doctor, and hospital data |
| `VISITS_TRANSFORM_SP` | `VISITS_TRANSFORM` | Combines visit, patient, doctor, and hospital data |

## Why Stored Procedures Are Used

Stored procedures package transformation SQL into reusable database objects.

Instead of putting all transformation SQL directly inside Airflow, Airflow can call the stored procedures in order. This keeps orchestration and transformation responsibilities separate:

```text
Airflow = when and in what order tasks run
Snowflake stored procedures = what transformation SQL runs
```

## Bronze to Silver Transformation Pattern

The Silver procedures read from raw Bronze tables and create transformed Silver tables.

Examples of Silver transformations in this project include:

- splitting full names into first and last names
- converting date strings into date values
- converting cost strings into numeric values
- joining related source tables
- renaming columns into clearer analytical names

## Implementation Note

This project uses `TRY_TO_DATE()` and `TRY_TO_DECIMAL()` for type conversion.

These functions are more forgiving than direct casts because malformed source values return `NULL` instead of failing the full transformation.

## Current Status

Created:

- `PATIENTS_TRANSFORM_SP`
- `TREATMENTS_TRANSFORM_SP`
- `VISITS_TRANSFORM_SP`

The procedures define the transformation logic. The transformed Silver tables are created when the procedures are called.

## Validation

Validation is complete when all three stored procedures exist in:

```text
AIRFLOW_DB.SILVER
```

The validation query used is:

```sql
SHOW PROCEDURES IN SCHEMA AIRFLOW_DB.SILVER;
```
