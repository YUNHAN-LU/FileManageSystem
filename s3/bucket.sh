#!/usr/bin/env bash

awslocal s3api create-bucket --bucket oss-bucket --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2
awslocal s3api put-object --bucket oss-bucket --key Documents/ --content-length 0
awslocal s3api put-object --bucket oss-bucket --key Images/ --content-length 0
awslocal s3api put-object --bucket oss-bucket --key Images/123 --content-length 0
awslocal s3api put-bucket-cors --bucket oss-bucket --cors-configuration '{"CORSRules":[{"AllowedHeaders":["*"],"AllowedMethods":["GET","POST","PUT"],"AllowedOrigins":["http://localhost:3000"],"ExposeHeaders":["ETag"]}]}'