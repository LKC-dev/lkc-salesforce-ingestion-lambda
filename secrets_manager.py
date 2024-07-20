import json
import logging
import boto3
import base64
from botocore.exceptions import ClientError
from settings import AWS_SECRET

logging.getLogger('botocore').setLevel(logging.ERROR)

def get_secret(secret_name):
    """
    Retrieves the value of a secret from AWS Secrets Manager.
cd
    Args:
        secret_name (str): The name or ARN of the secret.

    Returns:
        str: The value of the secret.

    Raises:
        ClientError: If an error occurs while retrieving the secret.
    """
    region_name = "us-east-2"

    # Get AWS credentials from the specified secret
    aws_secret_str = get_secret_value(AWS_SECRET, region_name)
    aws_credentials = json.loads(aws_secret_str)

    # Create a Secrets Manager client using the retrieved AWS credentials
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=aws_credentials['Access Key Id'],
        aws_secret_access_key=aws_credentials['Secret Access Key']
    )

    # Retrieve the requested secret
    return get_secret_value(secret_name, region_name, client)

def get_secret_value(secret_name, region_name, client=None):
    """
    Helper function to retrieve a secret value from AWS Secrets Manager.

    Args:
        secret_name (str): The name or ARN of the secret.
        region_name (str): The AWS region where the secret is stored.
        client (boto3.client, optional): A preconfigured boto3 client for Secrets Manager.

    Returns:
        str: The value of the secret.

    Raises:
        ClientError: If an error occurs while retrieving the secret.
    """
    if client is None:
        # Create a Secrets Manager client using default credentials
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        logging.error(f"Unable to retrieve secret {secret_name}: {e}")
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])
