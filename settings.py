AWS_SECRET = "prod/SAAWS"
MWAA_ENVIRONMENT_NAME = 'v4data-mwaa-production-environment'
DAG_NAME = 'dag_api_salesforce_history_lead_opportunity_raw_trusted'
BUCKET_NAME = 'lkc-datalake-prd'
SALESFORCE_OBJECT_NAME = 'Lead'
INCREMENTAL_COLUMN = 'LastModifiedDate'
SELECTED_COLUMNS: [
  'Id',
  'IsDeleted',
  'LastName',
  'Name',
  'RecordTypeId',
  'Company',
  'Phone',
  'MobilePhone',
  'Email',
  'PhotoUrl',
  'Description',
  'LeadSource',
  'Status',
  'NumberOfEmployees',
  'OwnerId',
  'IsConverted',
  'IsUnreadByOwner',
  'CreatedDate',
  'CreatedById',
  'LastModifiedDate',
  'LastModifiedById',
  'SystemModstamp',
  'LastActivityDate',
  'FirstCallDateTime',
  'FirstEmailDateTime',
  'ActivityMetricId'
  ]