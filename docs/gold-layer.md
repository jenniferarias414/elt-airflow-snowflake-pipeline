# Gold Layer Objects

## Purpose

The Gold layer contains curated, analytics-ready aggregate logic.

In this project, the Gold layer is created through Snowflake stored procedures that read from Silver transformed tables and create summary tables for reporting-style use cases.

## Stored Procedures Created

| Stored Procedure | Creates Table | Purpose |
|---|---|---|
| `CITY_HEALTHCARE_ACCESS_AGG_SP` | `CITY_HEALTHCARE_ACCESS_AGG` | Summarizes patient and hospital access by city |
| `HOSPITAL_PERFORMANCE_AGG_SP` | `HOSPITAL_PERFORMANCE_AGG` | Summarizes visits, treatments, average cost, and success rate by hospital |
| `PATIENT_VISIT_SUMMARY_AGG_SP` | `PATIENT_VISIT_SUMMARY_AGG` | Summarizes each patient's first visit, last visit, total visits, and visit spacing |
| `PATIENT_VALUE_AGG_SP` | `PATIENT_VALUE_AGG` | Summarizes patient treatment counts and cost metrics |

## Gold Layer Pattern

The Gold procedures read from Silver transformed tables and create aggregate tables.

```text
Silver transformed tables
        ↓
Gold aggregation stored procedures
        ↓
Gold analytics-ready tables
```

The Gold layer is where data becomes easier to consume for dashboards, reporting, and business analysis.

## Example Business Questions

The Gold layer supports questions such as:

- How many patients and hospitals are represented by city?
- Which hospitals have the most visits or treatments?
- What is the average treatment cost by hospital?
- What is the treatment success rate by hospital?
- How often do patients return for visits?
- Which patients have the highest total treatment cost?

## Implementation Note

The Gold procedures use aggregate functions such as:

- `COUNT`
- `COUNT(DISTINCT ...)`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- `ROUND`

The hospital success rate calculation uses `NULLIF(COUNT(*), 0)` to avoid divide-by-zero errors.

## Current Status

Created:

- `CITY_HEALTHCARE_ACCESS_AGG_SP`
- `HOSPITAL_PERFORMANCE_AGG_SP`
- `PATIENT_VISIT_SUMMARY_AGG_SP`
- `PATIENT_VALUE_AGG_SP`

The procedures define the aggregation logic. The Gold aggregate tables are created when the procedures are called.

## Validation

Validation is complete when all four stored procedures exist in:

```text
AIRFLOW_DB.GOLD
```

The validation query used is:

```sql
SHOW PROCEDURES IN SCHEMA AIRFLOW_DB.GOLD;
```
