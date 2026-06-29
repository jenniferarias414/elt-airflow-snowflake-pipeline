# AWS S3 and Snowflake Storage Integration

## Purpose

This section connects Snowflake to the project S3 data bucket using a Snowflake storage integration and an AWS IAM role.

The integration allows Snowflake to access staged files in S3 without storing raw AWS access keys in the Snowflake stage definition.

```text
Snowflake Storage Integration
        ↓
AWS IAM Role Trust Policy
        ↓
S3 Data Bucket
        ↓
Snowflake External Stage
```

## Objects Created

| Platform | Object | Purpose |
|---|---|---|
| Snowflake | `AIRFLOW_DB` | Project database |
| Snowflake | `BRONZE` schema | Raw/landing data layer |
| Snowflake | `SILVER` schema | Cleaned/transformed layer |
| Snowflake | `GOLD` schema | Curated analytics layer |
| Snowflake | `AIRFLOW_S3_INT` | Storage integration for S3 access |
| Snowflake | `AIRFLOW_S3_STAGE` | External stage pointing to the S3 data bucket |
| AWS IAM | Updated trust policy | Allows the Snowflake-generated principal to assume the IAM role |

## Integration Flow

The Snowflake storage integration stores the AWS IAM role ARN and allowed S3 locations. After the integration is created, Snowflake provides two important property values:

```text
STORAGE_AWS_IAM_USER_ARN
STORAGE_AWS_EXTERNAL_ID
```

Those values are added to the AWS IAM role trust policy. This completes the trust relationship between Snowflake and AWS.

## Why the Trust Policy Is Updated in Two Steps

The IAM role is created first with a temporary trust policy because the final Snowflake-generated principal and external ID do not exist until after the Snowflake storage integration is created.

The final setup flow is:

```text
Create AWS IAM role
Create Snowflake storage integration
Capture Snowflake-generated trust values
Update AWS IAM role trust policy
Create Snowflake external stage
Validate stage access
```

## Important Implementation Detail

The two Snowflake values are not separate SQL commands. They are properties returned by:

```sql
DESC INTEGRATION AIRFLOW_S3_INT;
```

The values can be located in the result table or filtered using `RESULT_SCAN`.

## Validation

Validation is complete when:

- `DESC INTEGRATION AIRFLOW_S3_INT` returns Snowflake-generated AWS trust values.
- The AWS IAM trust policy is updated with those values.
- `LIST @AIRFLOW_DB.BRONZE.AIRFLOW_S3_STAGE;` runs without an access error.

## Screenshot Evidence

Recommended screenshots for this section:

```text
05-snowflake-database-schemas-created.png
06-snowflake-storage-integration-created.png
07-aws-iam-trust-policy-updated-for-snowflake.png
08-snowflake-external-stage-list-success.png
```
