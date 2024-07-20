import json
import urllib.request
from secrets_manager import get_secret

class salesforce:
    def __init__(self):
        """
        Initialize the Salesforce object and refreshes the access token.
        """

        self.token = self.refresh_force_token()

    def refresh_force_token(self):
        """
        Refreshes the Salesforce access token using the API token from secrets manager.
        
        Returns:
            str: The access token.
        """

        url = json.loads(get_secret("prod/salesforce-api-token"))['url']
        payload = json.loads(get_secret("prod/salesforce-api-token"))['payload']
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': json.loads(get_secret("prod/salesforce-api-token"))['cookie']
        }
        try:
            req = urllib.request.Request(url, data=payload.encode(), headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                if response.getcode() != 200:
                    raise Exception(f'Failed to connect code: {response.getcode()}')
                request = json.loads(response.read())
                return request['access_token']
        except Exception as e:
            raise e

    def pull_data(self, selected_columns: str, incremental_column: str, salesforce_object_name: str) -> list:
        """
        Pulls data from Salesforce based on the specified columns, object name, and incremental column.
        
        Args:
            selected_columns (str): Comma-separated list of columns to retrieve.
            incremental_column (str): The incremental column to filter data.
            salesforce_object_name (str): The Salesforce object name to query.
        
        Returns:
            list: List of records retrieved from Salesforce in JSON format.
        """

        query = f"SELECT {', '.join(selected_columns)} FROM {salesforce_object_name} WHERE {incremental_column} >= LAST_N_DAYS:1"
        nextRecordsUrl = f'services/data/v54.0/query?q={query}'
        all_records = []

        while True:
            url = f"https://somecompany.my.salesforce.com/{nextRecordsUrl}"
            headers = {
                'Authorization': f'Bearer {self.token}'
            }

            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                dados = json.loads(response.read())

                if 'records' in dados:
                    all_records.extend(dados['records'])

                if 'nextRecordsUrl' in dados:
                    nextRecordsUrl = dados['nextRecordsUrl']
                else:
                    break

        return all_records