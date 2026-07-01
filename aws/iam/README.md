# AWS IAM Templates

This folder contains sanitized IAM policy examples used by the project.

The real project-specific IAM policy documents are stored under `notes/private/` because they may contain account-specific ARNs, bucket names, Snowflake external IDs, or other private values.

## Templates Included

| File | Purpose |
|---|---|
| `snowflake-trust-policy-template.json` | Shows the trust policy pattern Snowflake uses to assume an AWS IAM role |
| `snowflake-s3-read-policy-template.json` | Shows scoped S3 read access for Snowflake |
| `mwaa-scoped-s3-policy-template.json` | Shows scoped S3 access for the MWAA execution role |

## Why Templates Are Used

The project uses scoped permissions instead of broad account-level S3 access.

This keeps IAM access focused on the buckets required for the pipeline:

```text
Snowflake role → read project data bucket
MWAA execution role → read Airflow files bucket and read/write project data bucket
```

These templates are intentionally generic and should be customized for a real AWS account before use.
