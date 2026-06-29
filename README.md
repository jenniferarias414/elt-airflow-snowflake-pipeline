# ELT Data Pipeline with Airflow and Snowflake

This project builds an ELT-style data pipeline using AWS S3, Snowflake, and Apache Airflow.

The pipeline stages data in Amazon S3, loads it into Snowflake, transforms it through Bronze, Silver, and Gold layers, and uses Airflow to orchestrate the workflow.

## Project Architecture

```text
HTTP/API Source
      ↓
Python extraction
      ↓
Amazon S3 landing bucket
      ↓
Snowflake Bronze layer
      ↓
Snowflake Silver layer
      ↓
Snowflake Gold layer
      ↓
Airflow DAG orchestration
```

## Project Goal

The goal is to understand how a modern ELT workflow connects cloud storage, cloud data warehousing, and workflow orchestration.

This project focuses on:

- AWS IAM role setup for Snowflake access
- S3 bucket creation and file staging
- Snowflake external stage and layered table design
- Bronze, Silver, and Gold data modeling
- Managed Apache Airflow orchestration
- End-to-end validation and cleanup

## Current Status

Project setup started. AWS and Snowflake resources will be created in later phases and documented as the build progresses.
