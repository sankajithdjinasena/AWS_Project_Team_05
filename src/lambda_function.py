"""
AWS Lambda Function: Automated Telco Dataset Validator
AWS Project Group 07

Triggered by S3 ObjectCreated event on s3://telecom-churn-analytics-team07/raw/*.csv
Performs:
1. File validation (non-empty check, CSV extension check)
2. Schema & column existence check (verifies required fields like customerID, Churn, TotalCharges)
3. Data quality logging to AWS CloudWatch Logs
"""

import json
import logging
import urllib.parse
import boto3
import csv

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

# List of mandatory columns for Telco Customer Churn dataset validation
REQUIRED_COLUMNS = [
    'customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents',
    'tenure', 'PhoneService', 'MultipleLines', 'InternetService',
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
    'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn'
]

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event, indent=2))
    
    # Extract S3 bucket name and key from the event
    try:
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')
        logger.info(f"Processing object s3://{bucket}/{key}")
    except Exception as e:
        logger.error(f"Error parsing S3 event: {str(e)}")
        raise e

    # Check file format extension
    if not key.endswith('.csv'):
        logger.warning(f"File {key} is not a CSV. Validation skipped.")
        return {'statusCode': 400, 'body': json.dumps('File must be a CSV.')}

    try:
        # Fetch object from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        lines = response['Body'].read().decode('utf-8').splitlines()
        
        if not lines:
            logger.error("Uploaded file is completely empty!")
            return {'statusCode': 400, 'body': json.dumps('Uploaded file is empty.')}
        
        # Read header row
        reader = csv.reader(lines)
        header = next(reader)
        logger.info(f"Header columns found: {header}")

        # Validate schema against required columns
        missing_columns = [col for col in REQUIRED_COLUMNS if col not in header]
        
        if missing_columns:
            logger.error(f"DATA QUALITY FAILURE: Missing columns: {missing_columns}")
            return {
                'statusCode': 422,
                'body': json.dumps({'status': 'FAILED', 'missing_columns': missing_columns})
            }
        
        total_rows = len(lines) - 1
        logger.info(f"DATA QUALITY SUCCESS: Validated schema successfully! Found {total_rows} records.")

        # Flag blank TotalCharges occurrences in logging
        blank_total_charges_count = 0
        total_charges_idx = header.index('TotalCharges')
        for row in reader:
            if len(row) > total_charges_idx and (row[total_charges_idx] == '' or row[total_charges_idx] == ' '):
                blank_total_charges_count += 1
                
        if blank_total_charges_count > 0:
            logger.warning(f"Data Quality Alert: Identified {blank_total_charges_count} rows with blank 'TotalCharges'. Needs imputation.")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'SUCCESS',
                'message': 'Dataset schema and data quality check passed.',
                'records_count': total_rows,
                'blank_total_charges_flagged': blank_total_charges_count
            })
        }

    except Exception as e:
        logger.error(f"Error reading file from S3: {str(e)}")
        raise e
