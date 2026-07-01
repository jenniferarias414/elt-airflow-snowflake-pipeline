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

---

## Bronze Layer Design

The Bronze layer is the first Snowflake layer in this project.

Its purpose is to receive raw data with minimal transformation. This creates a stable landing area before applying cleanup or business rules.

The Bronze tables use `STRING` data types because source files often arrive as text. Keeping raw fields as strings makes the first load more forgiving and preserves the original source values.

Later layers can apply stricter data types:

```text
Bronze: raw strings
Silver: cleaned and typed data
Gold: curated analytics-ready data
```

This pattern makes troubleshooting easier because the raw source values remain available if a transformation issue appears later.

---

## Silver Layer Design

The Silver layer improves raw Bronze data by applying structure, cleanup, type conversion, and joins.

In this project, Silver transformations are stored as Snowflake stored procedures. This keeps the SQL transformation logic inside Snowflake while allowing Airflow to orchestrate when each procedure runs.

The pattern is:

```text
Bronze raw tables
      ↓
Silver stored procedures
      ↓
Silver transformed tables
```

## Why Use Stored Procedures

Stored procedures are reusable database routines.

For this project, they help separate responsibilities:

```text
Airflow controls workflow order.
Snowflake performs data transformations.
```

This is useful because the transformation SQL stays close to the data warehouse, while Airflow focuses on scheduling and dependencies.

## Safer Type Conversion

The Bronze layer stores raw values as strings. The Silver layer begins converting those strings into useful data types.

This project uses `TRY_TO_DATE()` and `TRY_TO_DECIMAL()` for conversions. These functions help prevent one bad source value from breaking the entire transformation.

For example:

```text
Bronze DOB string → Silver patient date of birth
Bronze cost string → Silver numeric treatment cost
```

---

## Gold Layer Design

The Gold layer is the curated analytics layer.

While Bronze keeps raw source-shaped data and Silver creates cleaned transformed data, Gold creates business-friendly summaries.

The pattern is:

```text
Bronze = raw landing
Silver = cleaned and joined
Gold = aggregated and analytics-ready
```

Gold objects are often the closest layer to dashboards, reports, and business-facing metrics.

## Aggregate Tables

An aggregate table summarizes detailed records into higher-level metrics.

In this project, the Gold procedures create summaries such as:

- patients by city
- hospital performance
- patient visit history
- patient treatment value

These tables are easier to query than raw transactional tables because common calculations are already prepared.

## Stored Procedures in the Gold Layer

The Gold procedures package aggregation SQL into reusable database routines.

This allows Airflow to call the procedures as pipeline tasks instead of embedding all aggregation SQL directly in the DAG.

The responsibility split remains:

```text
Airflow = orchestrates task order
Snowflake = executes transformation and aggregation logic
```

## Why Gold Tables Depend on Silver Tables

Gold procedures read from Silver transform tables, not directly from Bronze raw tables.

This keeps the Gold layer focused on analytics rather than raw cleanup.

The dependency chain is:

```text
Bronze raw tables
      ↓
Silver transformed tables
      ↓
Gold aggregate tables
```


### Filtering Snowflake `SHOW` Results

Snowflake `SHOW` commands can return system or built-in objects along with project-created objects. In this project, custom stored procedures are identified by:

```text
schema_name = GOLD
is_builtin = N
```

Filtering `SHOW PROCEDURES` output makes validation screenshots clearer and keeps the focus on project-created objects.

---

## Public Templates vs Private Configuration

This repository separates reusable examples from account-specific configuration.

Public-safe examples are kept in folders such as:

```text
aws/iam/
docs/
learning-notes/
snowflake/sql/
```

Private or account-specific values are kept under:

```text
notes/private/
```

This separation keeps the repository useful for review and learning while avoiding accidental exposure of AWS account IDs, role ARNs, Snowflake external IDs, credentials, or private troubleshooting notes.

---

## Managed Apache Airflow on AWS

Amazon MWAA is AWS-managed Apache Airflow. It provides the Airflow scheduler, workers, metadata database, logs, and web UI without requiring a manually managed Airflow server.

In this project, Airflow is the orchestrator.

It does not replace Snowflake or S3.

```text
S3 = stores files
Snowflake = stores and transforms data
Airflow = schedules and coordinates tasks
```

## DAG Files and Requirements

MWAA reads DAG files from an S3 `dags/` folder.

The `requirements.txt` file is separate because it defines Python packages that must be installed into the Airflow environment.

```text
dags/            = workflow definitions
requirements.txt = Python dependencies
```

## MWAA Execution Role

The MWAA execution role controls what the Airflow environment can access in AWS.

For this project, the execution role needs scoped access to:

- read DAG and requirements files
- read/write project data files
- write logs through AWS-managed MWAA permissions

Using scoped bucket access keeps the lab closer to least-privilege design.

