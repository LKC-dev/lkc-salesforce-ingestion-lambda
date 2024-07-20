import boto3
import urllib.request
import base64
import ast

def start_mwaa_dag(mwaa_env_name: str, dag_name: str) -> bytes:
    """
    Starts an MWAA DAG by triggering it with the provided environment name and DAG name.
    
    Args:
        mwaa_env_name (str): The name of the MWAA environment.
        dag_name (str): The name of the DAG to trigger.
        
    Returns:
        bytes: The decoded output from triggering the DAG.
    """
    client = boto3.client('mwaa')
    
    mwaa_cli_token = client.create_cli_token(
        Name=mwaa_env_name
    )

    url = f"https://{mwaa_cli_token['WebServerHostname']}/aws_mwaa/cli"
    payload = f'dags trigger {dag_name}'.encode()
    
    headers = {
        'Authorization': f'Bearer {mwaa_cli_token["CliToken"]}',
        'Content-Type': 'text/plain'
    }
    
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    with urllib.request.urlopen(req) as res:
        data = res.read()
        dict_str = data.decode("UTF-8")
        mydata = ast.literal_eval(dict_str)
        return base64.b64decode(mydata['stdout'])