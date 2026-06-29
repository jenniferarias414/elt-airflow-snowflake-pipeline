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

---

## Implementation Choices Worth Noting

### Scoped S3 Access Instead of Broad Bucket Permissions

The Snowflake IAM role is configured to use a bucket-scoped S3 policy instead of broad S3 access.

This keeps the role focused on the project data bucket and supports a better least-privilege pattern:

```text
Snowflake storage integration → IAM role → specific S3 data bucket
```

This approach helps make the access pattern easier to reason about and avoids giving the role unnecessary access to unrelated S3 buckets.

### Separate Buckets for Airflow Files and Pipeline Data

This project separates Airflow files from pipeline data:

```text
jennyarias-elt-airflow-files   # DAG files and requirements.txt
jennyarias-elt-airflow-data    # raw/staged/archive data files
```

Keeping these concerns separate makes the project easier to manage:

- Airflow files support orchestration.
- Data bucket files support ingestion and loading.
- Cleanup and troubleshooting are more focused because each bucket has a clear purpose.

### Data Bucket Prefixes

The data bucket uses logical prefixes:

```text
raw/       incoming source files
staged/    files prepared for Snowflake loading
archive/   optional processed-file storage
```

S3 does not use folders in the same way a local computer does, but prefixes create a folder-like structure that makes object storage easier to navigate and document.

### Airflow Requirements File at the Bucket Root

The `requirements.txt` file is uploaded to the root of the Airflow files bucket, while DAG files belong under the `dags/` prefix.

This keeps the Airflow dependency file separate from the DAG code:

```text
requirements.txt
dags/
```

The requirements file defines Python packages the Airflow environment needs, while the DAG folder contains workflow definitions.

### Manual Builds and Controlled Resource Usage

For a learning project, manual setup and manual validation make the workflow easier to observe and troubleshoot.

Later, the same pattern could be automated further with infrastructure-as-code or CI/CD tooling. For this build, the priority is understanding each resource and validating the end-to-end flow before cleanup.

---

## Snowflake and AWS Trust Flow

A Snowflake storage integration does not directly copy files by itself. It stores configuration that allows Snowflake to authenticate to AWS through an IAM role.

The setup works in two directions:

```text
Snowflake knows which AWS role to use.
AWS knows which Snowflake-generated principal is allowed to assume that role.
```

This is why the role setup happens in two passes:

1. Create a placeholder IAM role in AWS.
2. Create the storage integration in Snowflake.
3. Copy Snowflake-generated values back into the AWS trust policy.
4. Create an external stage that uses the storage integration.

## Storage Integration vs External Stage

The storage integration answers:

```text
How is Snowflake allowed to authenticate to cloud storage?
```

The external stage answers:

```text
Which S3 location should Snowflake read from?
```

Keeping these separate makes the design cleaner because multiple stages can use the same storage integration as long as their URLs match the allowed storage locations.

## Why the Stage Validation Matters

The `LIST` command confirms that Snowflake can reach the S3 location through the storage integration and IAM role.

A successful `LIST` does not mean data has been loaded yet. It means the access path is working:

```text
Snowflake stage → storage integration → IAM role → S3 bucket
```

This is an important checkpoint before creating the Bronze layer load objects.

