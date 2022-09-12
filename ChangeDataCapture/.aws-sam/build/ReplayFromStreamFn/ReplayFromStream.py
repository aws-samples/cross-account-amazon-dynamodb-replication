import os
import json
import boto3

def lambda_handler(event, context):

    # Environment Variables
    target_aws_account_num = os.environ['TARGET_AWS_ACCOUNT_NUMBER']
    target_role_name = os.environ['TARGET_ROLE_NAME']
    target_ddb_name = os.environ['TARGET_DYNAMODB_NAME']
    target_ddb_region = os.environ['TARGET_REGION']

    role_arn = "arn:aws:iam::%s:role/%s" % (target_aws_account_num,target_role_name)

    sts_response = get_credentials(role_arn)
    
    dynamodb = boto3.client('dynamodb', region_name=target_ddb_region,
                            aws_access_key_id = sts_response['AccessKeyId'],
                            aws_secret_access_key = sts_response['SecretAccessKey'],
                            aws_session_token = sts_response['SessionToken'])

 
    
    Records = event['Records']

    for record in Records:
        # Peter added for omnivorous mode - since we always use the same table name
        # we can use the record to determine the destination table name
        # Example eventSourceARN = arn:aws:dynamodb:us-east-1:682422205370:table/mx_admin_dmarc_copy/stream/2022-08-06T23:44:43.890
        target_ddb_name = record['eventSourceARN'].split('/')[1]
        # End Peter added for omnivorous mode
        event_name = record['eventName']
        
        if event_name == 'REMOVE':
            response = dynamodb.delete_item(TableName=target_ddb_name,Key=record['dynamodb']['Keys'])
        else:
            response = dynamodb.put_item(TableName=target_ddb_name,Item=record['dynamodb']['NewImage'])
            
def get_credentials(role_arn):
    # create an STS client object that represents a live connection to the 
    # STS service
    sts_client = boto3.client('sts')

    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    assumed_role_object=sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="cross_acct_lambda"
    )

    # From the response that contains the assumed role, get the temporary 
    # credentials that can be used to make subsequent API calls
    sts_response=assumed_role_object['Credentials']
    return sts_response
