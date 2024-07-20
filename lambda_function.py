import json
import logging
from datetime import datetime, timedelta, timezone
import boto3
from salesforce import salesforce
from start_dag import start_mwaa_dag
from settings import MWAA_ENVIRONMENT_NAME, DAG_NAME, BUCKET_NAME, SALESFORCE_OBJECT_NAME, INCREMENTAL_COLUMN, SELECTED_COLUMNS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

s3 = boto3.client('s3')

extraction_date = datetime.now(timezone(timedelta(hours=-3))).strftime("%Y_%m_%d_%Hh")

def lambda_handler(event, context):
    try:
        salesforce_api = salesforce()
        data = salesforce_api.pull_data(SELECTED_COLUMNS, INCREMENTAL_COLUMN, SALESFORCE_OBJECT_NAME)
        if data is None:
            logger.error(f"Failed to get {SALESFORCE_OBJECT_NAME} object from Salesforce.")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'Failed to get {SALESFORCE_OBJECT_NAME} object from Salesforce'})
            }

        json_data = json.dumps(data)
                
        file_path = f'salesforce/raw/{extraction_date}_salesforce_{SALESFORCE_OBJECT_NAME}.json'
        logger.info(f"Storing data in S3 Bucket {file_path}.")

        s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=json_data)
        
        logger.info("Lambda execution successfull.")

        start_mwaa_dag(MWAA_ENVIRONMENT_NAME, DAG_NAME)
        logger.info(f"Started MWAA DAG: {MWAA_ENVIRONMENT_NAME}, {DAG_NAME}")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Data ingested and stored in S3 Raw Bucket. Started MWAA DAG: {MWAA_ENVIRONMENT_NAME}.{DAG_NAME}'})
        }
    except Exception as e:
        logger.error(f"Lambda execution failed: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Lambda execution failed'})
        }
