#  Cross Account Amazon DynamoDB Replication

  
This repository accompanies the [Cross Account Amazon DynamoDB Replication](https://aws.amazon.com/blogs/database/cross-account-replication-with-amazon-dynamodb) blog post. It contains **two** [AWS Serverless Application Model (AWS SAM)](https://aws.amazon.com/serverless/sam/) templates. 

1. First template deploys an [AWS Glue](https://aws.amazon.com/glue) job used for loading the data from the source DynamoDB table to the target DynamoDB table. If you are using the native [DynamoDB export feature](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBPipeline.html), do not use this template. Only use this template if the source DynamoDB table size is less than 140GB and you are using AWS Glue job for export and import.
2. The second template deploys one [AWS Lambda](https://aws.amazon.com/lambda) function that reads from source DynamoDB stream and replicates the changes to the target [Amazon DyanmoDB](https://aws.amazon.com/dynamodb/) table in a different AWS account.


```bash
├── README.MD <-- This instructions file

├── InitialLoad <-- The SAM template for Initial Load using Glue for import and export

├── ChangeDataCapture <-- The SAM template for Change Data Capture (CDC)

├── InitialMigrationWithNativeExport <-- Sample Glue code to help you get started. Bash script to change the owner of the objects in the target S3 bucket.

```

## General Requirements

* AWS CLI already configured with Administrator permission
* [Install SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) if you do not have it.
* Source and target tables created in DynamoDB
* Target IAM role created with permissions to write to target DynamoDB table
* **For Change Data Capture**, DynamoDB streams should be enabled on source table

## Installation Instructions

Clone the repo onto your local development machine using `git clone <repo url>`.


### Initial Load

  
1. From the command line, change directory to SAM template directory for Initial Load

```

cd InitialLoad

```


2. Run the below commands to deploy the template

```

sam build

sam deploy --guided

```

Follow the prompts in the deploy process to set the stack name, AWS Region and other parameters.


#### Initial Load Parameter Details


*   **TargetDynamoDBTable**: Target DynamoDB Table name
*   **TargetAccountNumber**: Target AWS Account Number
*   **TargetRoleName**: Target IAM Role name to be assumed by the Glue job
*   **TargetRegion**: The region for the target DynamoDB table
*   **SourceDynamoDBTable**: Source DynamoDB Table name
*   **WorkerType**:  The type of predefined worker that is allocated when a job runs. Accepts a value of Standard, G.1X, or G.2X.
*   **NumberOfWorkers**: The number of workers of a defined workerType that are allocated when a job runs.
*   **JobName**: Name of the Glue Job


### Change Data Capture (CDC)

1. From the command line, change directory to SAM template directory for Initial Load

```

cd ChangeDataCapture

```


2. Run the below commands to deploy the template

```

sam build

sam deploy --guided

```

Follow the prompts in the deploy process to set the stack name, AWS Region and other parameters.



#### CDC Parameter Details


*   **TargetDynamoDBTable**: Target DynamoDB Table name
*   **TargetAccountNumber**: Target AWS Account Number
*   **TargetRoleName**: Target IAM Role name to be assumed by Lambda function
*   **TargetRegion**: The region for the target DynamoDB table
*   **MaximumRecordAgeInSeconds**: The maximum age (in seconds) of a record in the stream that Lambda sends to your function.
*   **SourceTableStreamARN**: Source DynamoDB table stream ARN

  
## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.

