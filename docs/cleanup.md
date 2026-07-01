# Cleanup Notes

## Purpose

This project used temporary AWS and Snowflake resources for a hands-on ELT pipeline build.

After the pipeline was validated and the repository was pushed, the cloud resources were cleaned up to avoid ongoing costs.

## AWS Resources Cleaned Up

The following AWS resources were removed:

| Resource Type | Resource |
|---|---|
| Amazon MWAA | `jenny-elt-airflow` environment |
| CloudFormation | `MWAA-VPC` networking stack |
| Amazon S3 | `jennyarias-elt-airflow-files` bucket |
| Amazon S3 | `jennyarias-elt-airflow-data` bucket |
| IAM Role | Snowflake S3 access role |
| IAM Role | MWAA execution role |
| CloudWatch Logs | MWAA/Airflow log groups, where applicable |

## Cleanup Order

The cleanup was performed in this order:

```text
1. Delete MWAA environment
2. Delete MWAA VPC CloudFormation stack
3. Delete S3 bucket contents and buckets
4. Delete CloudWatch log groups
5. Delete IAM roles and inline policies
6. Optionally drop Snowflake database objects
```

MWAA was deleted before the S3 buckets because the Airflow environment references the S3 bucket that stores DAG files and requirements.

## Issue Encountered

The MWAA VPC CloudFormation stack initially failed to delete because the VPC still had dependent security groups.

After MWAA finished deleting, two leftover MWAA security groups were removed manually, and the CloudFormation stack deletion completed successfully.

## Final AWS Validation

Cleanup was validated by confirming:

```text
MWAA environments: []
No project S3 buckets found
MWAA-VPC stack not found
Snowflake IAM role not found
MWAA IAM role not found
```

## Snowflake Cleanup

After screenshots and validation were captured, the Snowflake project database can be removed with:

```sql
USE ROLE ACCOUNTADMIN;
DROP DATABASE IF EXISTS AIRFLOW_DB;
```

## Cost Control Note

Amazon MWAA can create ongoing charges while the environment exists. For learning projects, the environment should be deleted after validation is complete.
