cross-account-dynamo-migration
cross-account-dynamo-replication

SOURCE
682422205370
arn:aws:dynamodb:us-east-1:682422205370:table/mx_admin_dmarc_copy
arn:aws:dynamodb:us-east-1:682422205370:table/mx_admin_dmarc_copy/stream/2022-08-06T23:44:43.890

TARGET
233870680723
arn:aws:dynamodb:us-east-1:233870680723:table/mx_admin_dmarc_copy

TARGET_PROD
191686924229


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

# Dynamo Replication
----------------------------------------
`DEVS`
FUNCTION_NAME=cross-account-dynamo-replicatio-ReplayFromStreamFn-uumi33NY6SI5
`PROD`
FUNCTION_NAME=cross-account-dynamo-replicatio-ReplayFromStreamFn-HRHwfKyuZcJA

TABLE=mx_yaml_prod_DmarcAggregate_SenderIpAddress_Sub
### Set up Aliases to create the strem
alias create_stream="aws dynamodb update-table --stream-specification StreamEnabled=true,StreamViewType=NEW_IMAGE --table-name $TABLE"
alias check_stream="aws dynamodb describe-table --table-name $TABLE | grep TableStatus"
alias set_stream="STREAM_ARN=`aws dynamodb describe-table --table-name $TABLE | grep LatestStreamArn | sed  's/^.*arn/arn/'`"

### Set up an Alias to deploy the mapping
alias enable_mapping="aws lambda create-event-source-mapping \
--function-name $FUNCTION_NAME \
--batch-size 500 \
--maximum-batching-window-in-seconds 5 \
--starting-position LATEST \
--event-source-arn $STREAM_ARN "

### Finished product
`SET THE TABLE=`
aws dynamodb update-table --stream-specification StreamEnabled=true,StreamViewType=NEW_IMAGE --table-name $TABLE

aws dynamodb describe-table --table-name $TABLE | grep TableStatus

STREAM_ARN=`aws dynamodb describe-table --table-name $TABLE | grep LatestStreamArn | sed  's/^.*arn/arn/'`

UUID=`aws lambda create-event-source-mapping --function-name $FUNCTION_NAME --batch-size 1000 --starting-position TRIM_HORIZON --event-source-arn $STREAM_ARN | tail -1 | sed 's/.*UUID: //'`

aws lambda get-event-source-mapping --uuid $UUID


mx_yaml_prod_complaint_aggregate_mothly_rollup_oes
mx_yaml_prod_complaint_aggregate_monthly_rollup_oes
