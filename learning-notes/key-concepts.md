# Key Concepts

## ELT

ELT stands for Extract, Load, Transform.

In an ELT pattern, data is extracted from a source system, loaded into a data platform, and then transformed inside the data warehouse.

This differs from ETL, where data is usually transformed before being loaded into the final warehouse.

## Amazon S3

Amazon S3 is object storage. In this project, S3 acts as the landing area for raw or staged files before Snowflake loads them.

## Snowflake

Snowflake is the cloud data warehouse used for storing and transforming the data.

This project uses a layered design:

```text
Bronze → Silver → Gold
```

## Bronze Layer

The Bronze layer usually stores raw or lightly processed data close to the source format.

## Silver Layer

The Silver layer usually applies cleaning, standardization, type casting, deduplication, and business rules.

## Gold Layer

The Gold layer usually contains curated tables or views that are easier for analytics, reporting, or downstream consumption.

## Apache Airflow

Apache Airflow is a workflow orchestration tool. It is used to schedule and coordinate tasks.

In this project, Airflow does not replace Snowflake. Airflow tells the pipeline what to run and in what order.

## DAG

DAG stands for Directed Acyclic Graph.

In Airflow, a DAG defines a workflow made of tasks and dependencies.

## Snowflake Storage Integration

A Snowflake storage integration is a secure Snowflake object that allows Snowflake to access external cloud storage like Amazon S3 without embedding raw AWS keys directly in the stage definition.

## IAM Role

An IAM role defines what actions an AWS service or external trusted service can perform.

In this project, Snowflake will use an IAM role to access files in a specific S3 bucket.
