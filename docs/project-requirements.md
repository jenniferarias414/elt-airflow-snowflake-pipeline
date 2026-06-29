# Project Requirements

## Project Name

ELT Data Pipeline with Airflow and Snowflake

## Starting Architecture

The project follows this high-level workflow:

```text
HTTP/API → Python → S3 → Snowflake Bronze → Snowflake Silver → Snowflake Gold
```

Apache Airflow orchestrates the pipeline steps.

## Technical Objectives

This project will create and validate:

1. An AWS IAM role for Snowflake S3 access.
2. An Amazon S3 bucket for staged source files.
3. A Snowflake storage integration for secure S3 access.
4. Snowflake Bronze, Silver, and Gold layer objects.
5. A managed Apache Airflow environment.
6. An Airflow connection to Snowflake.
7. An Airflow DAG that executes the pipeline steps.
8. Screenshots, validation notes, troubleshooting notes, and cleanup steps.

## Expected End State

The project is complete when:

- Files are staged in S3.
- Snowflake can access the S3 bucket through a storage integration.
- Bronze layer objects are created and loaded.
- Silver layer transformations run successfully.
- Gold layer objects are created for consumption.
- Airflow can orchestrate the workflow.
- AWS resources are documented and cleaned up.

## Out of Scope

This project is a learning lab, not a production deployment. It does not include:

- production-grade CI/CD
- Terraform automation
- long-running managed Airflow operations
- production secrets management hardening
- enterprise monitoring or alerting
