import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:mysecretpassword@db:5432/filesystem_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'admin')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'admin')
    S3_BUCKET = os.getenv('S3_BUCKET', 'oss-bucket')
    S3_ENDPOINT = os.getenv('S3_ENDPOINT', 'http://localstack:4566')
