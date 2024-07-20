# lkc-salesforce-ingestion-lambda

## Overview

This project demonstrates an automated data ingestion pipeline that integrates Salesforce with AWS services. The pipeline extracts data from Salesforce, stores it in an S3 bucket, and triggers a Managed Workflows for Apache Airflow (MWAA) DAG for further processing.

## Components

### 1. `salesforce.py`
Contains the `salesforce` class, which handles:
- Authentication with Salesforce and token refresh.
- Data extraction from Salesforce based on specified columns and conditions.

### 2. `secrets_manager.py`
Provides functions to retrieve secrets from AWS Secrets Manager, including:
- `get_secret`: Retrieves the value of a secret.
- `get_secret_value`: Helper function to fetch the secret value.

### 3. `settings.py`
Defines configuration constants used across the project, such as:
- AWS secret names.
- MWAA environment and DAG names.
- S3 bucket name.
- Salesforce object and columns to query.

### 4. `start_dag.py`
Contains the `start_mwaa_dag` function, which:
- Triggers a specified DAG in the MWAA environment.

### 5. `lambda_function.py`
Defines the AWS Lambda function, which:
- Initializes the Salesforce API client.
- Extracts data from Salesforce.
- Stores the extracted data in an S3 bucket.
- Triggers the MWAA DAG for further processing.

## How It Works

1. **Initialization**: The Lambda function initializes the Salesforce API client.
2. **Data Extraction**: The `pull_data` method in `salesforce.py` extracts data from Salesforce.
3. **Data Storage**: The extracted data is stored in an S3 bucket.
4. **DAG Trigger**: The `start_mwaa_dag` function triggers a DAG in the MWAA environment to process the stored data.

## Usage

To deploy and run this project, ensure you have the necessary AWS resources and permissions set up, including:
- AWS Secrets Manager for storing API tokens and credentials.
- An S3 bucket for storing extracted data.
- An MWAA environment with the specified DAG.

Deploy the Lambda function and configure it to trigger based on your desired schedule or events.

## Conclusion

This project provides a robust framework for automating data ingestion from Salesforce to AWS, leveraging AWS Lambda, S3, and MWAA for seamless data processing and integration.