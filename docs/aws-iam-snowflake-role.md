# AWS IAM Role for Snowflake S3 Access

## Purpose

This project requires an AWS IAM role that Snowflake can use to access files stored in Amazon S3.

The IAM role is part of the trust and permissions bridge between AWS and Snowflake.

```text
Snowflake Storage Integration → AWS IAM Role → S3 Bucket
```

## Course Step

The course creates a role named similar to:

```text
snowflakeloadrole
```

and attaches broad S3 permissions.

## Project Implementation

For this build, the role is named:

```text
snowflake-load-role-elt-airflow
```

A placeholder trust policy was used during initial role creation. This is because Snowflake generates the final trusted IAM user ARN and external ID after the Snowflake storage integration is created.

The role will be updated later with the Snowflake-generated values.

## Security Improvement

The course attaches `AmazonS3FullAccess` during role creation.

This project avoids that broad permission where possible. After the S3 bucket is created, a bucket-specific policy will be attached instead.

This keeps the role scoped to the project bucket rather than granting access to all S3 buckets in the AWS account.

## Current Status

Created:

- IAM role for Snowflake S3 access

Pending:

- S3 bucket creation
- bucket-scoped S3 policy
- Snowflake storage integration
- trust policy update using Snowflake-generated values
