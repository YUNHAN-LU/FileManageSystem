# app/services/s3.py
import boto3
from botocore.exceptions import ClientError

class S3Manager:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name, endpoint_url):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url
        )

        self.s3_resource = boto3.resource('s3', 
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url)
        self.bucket_name = bucket_name
    
    def upload_file(self, file_obj, filename, content_type):
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                filename,
                ExtraArgs={'ContentType': content_type}
            )
            return True
        except ClientError as e:
            print(f"Error uploading to S3: {e}")
            return False
        return True
    
    def get_presigned_url(self, filename):  
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name,'Key': filename},
                ExpiresIn=3600
            )

            return presigned_url
        except ClientError as e:
            print(f"Error downloading from S3: {e}")
            return False
        
    def create_folder(self, folder_name):
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=folder_name
            )
            return True
        except ClientError as e:
            print(f"Error creating folder in S3: {e}")
            return False
        
    def delete_folder(self, folder_name):
        try:
            
            bucket = self.s3_resource.Bucket(self.bucket_name)
            bucket.objects.filter(Prefix=folder_name).delete()
            return True
        except ClientError as e:
            print(f"Error deleting folder in S3: {e}")
            return False
    
    def delete_file(self, file_name):
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            return True
        except ClientError as e:
            print(f"Error deleting file in S3: {e}")
            return False