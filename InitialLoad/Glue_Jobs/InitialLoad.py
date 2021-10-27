import boto3
import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ['TARGET_DYNAMODB_NAME','SOURCE_DYNAMODB_NAME', 'TARGET_AWS_ACCOUNT_NUMBER', 'TARGET_ROLE_NAME', 'TARGET_REGION', 'WORKER_TYPE', 'NUM_WORKERS'])


target_aws_account_num = args['TARGET_AWS_ACCOUNT_NUMBER']
target_role_name = args['TARGET_ROLE_NAME']
target_ddb_name = args['TARGET_DYNAMODB_NAME']
source_region = boto3.session.Session().region_name
region = args['TARGET_REGION']
source_ddb_name = args['SOURCE_DYNAMODB_NAME']
worker_type = args['WORKER_TYPE']
num_workers = args['NUM_WORKERS']

target_role_arn="arn:aws:iam::"+target_aws_account_num+":role/"+target_role_name

if worker_type == 'G.2X':
    ddb_split= 16* (int(num_workers) - 1)

elif worker_type == 'G.1X':
    ddb_split= 8 * (int(num_workers) - 1)
else:
    num_executers = (int(num_workers) - 1) * 2 - 1
    ddb_split = 4 * num_executers

print(str(ddb_split))


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
glue_context= GlueContext(SparkContext.getOrCreate())
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

dyf = glue_context.create_dynamic_frame_from_options(
connection_type="dynamodb",
connection_options={
"dynamodb.region": source_region,
"dynamodb.splits": str(ddb_split),
"dynamodb.throughput.read.percent":"1.2",
"dynamodb.input.tableName": source_ddb_name
}
)
dyf.show()

sts_client = boto3.client('sts')
sts_response = sts_client.assume_role(RoleArn=target_role_arn, RoleSessionName='assume-role')

ddb_key = sts_response['Credentials']['AccessKeyId']
ddb_secret = sts_response['Credentials']['SecretAccessKey']
ddb_token = sts_response['Credentials']['SessionToken']

glue_context.write_dynamic_frame_from_options(
frame=dyf,
connection_type="dynamodb",
connection_options={
"dynamodb.region": region,
"dynamodb.output.tableName": target_ddb_name,
"dynamodb.awsAccessKeyId": ddb_key,
"dynamodb.awsSecretAccessKey": ddb_secret,
"dynamodb.awsSessionToken": ddb_token
}
)
job.commit()