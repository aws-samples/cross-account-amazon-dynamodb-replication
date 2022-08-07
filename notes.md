cross-account-dynamo-migration
cross-account-dynamo-replication

SOURCE
682422205370
arn:aws:dynamodb:us-east-1:682422205370:table/mx_admin_dmarc_copy
arn:aws:dynamodb:us-east-1:682422205370:table/mx_admin_dmarc_copy/stream/2022-08-06T23:44:43.890

TARGET
233870680723
arn:aws:dynamodb:us-east-1:233870680723:table/mx_admin_dmarc_copy
Cross-Account-Dynamo-Role

----------------------------------------

KeyName1=string,KeyName2=string

'TARGET_DYNAMODB_NAME','SOURCE_DYNAMODB_NAME', 'TARGET_AWS_ACCOUNT_NUMBER', 'TARGET_ROLE_NAME', 'TARGET_REGION', 'WORKER_TYPE', 'NUM_WORKERS']

aws glue start-job-run --job-name Initial_Load_Agg_Subject --arguments SOURCE_DYNAMODB_NAME=mx_yaml_prod_complaint_events,TARGET_DYNAMODB_NAME=mx_yaml_prod_complaint_events,TARGET_AWS_ACCOUNT_NUMBER=233870680723,TARGET_ROLE_NAME=Cross-Account-Dynamo-Role,TARGET_REGION=us-east-1,WORKER_TYPE=G.2X,NUM_WORKERS=145

mx_yaml_prod_complaint_aggregates failed because no more compute

4:47 leaving the computer

{
  "Domain": {
    "S": "mxtoolbox.com"
  },
  "CopyTo": {
    "S": "testing.com"
  },
  "CreatedOn": {
    "S": "2022-08-06T23:45:00Z"
  },
  "Description": {
    "S": "Initial test of replication"
  },
  "UserName": {
    "S": "peter@mxtoolbox.com"
  }
}

FUNCTION_NAME=cross-account-dynamo-replicatio-ReplayFromStreamFn-uumi33NY6SI5

aws dynamodb update-table --stream-specification StreamEnabled=true,StreamViewType=NEW_IMAGE --table-name mx_PerfUidTicks

aws dynamodb describe-table --table-name mx_PerfUidTicks | grep TableStatus
aws dynamodb describe-table --table-name mx_PerfUidTicks | grep LatestStreamArn

STREAM_ARN=arn:aws:dynamodb:us-east-1:682422205370:table/mx_PerfUidTicks/stream/2022-08-07T00:47:57.931


alias enable_mapping="aws lambda create-event-source-mapping \
--function-name $FUNCTION_NAME \
--batch-size 500 \
--maximum-batching-window-in-seconds 5 \
--starting-position LATEST \
--event-source-arn $STREAM_ARN"