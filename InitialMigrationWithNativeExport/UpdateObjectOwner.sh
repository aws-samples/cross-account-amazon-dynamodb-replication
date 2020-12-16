#!/bin/bash
input="/home/ec2-user/environment/file.txt"
while IFS= read -r line
do
aws s3api put-object-acl --bucket <nameofyourbucket> --key "$line" --acl
bucket-owner-full-control
echo "$line"
done < "$input"