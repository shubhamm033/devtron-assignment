from django.conf import settings
import boto3


class S3:

    def __init__(self):

        # s3 client

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME
        )

    def fetch_details_from_s3(self, folders=None):

        if folders is None:
            # fetch all the folders in the bucket
            paginator = self.s3_client.get_paginator('list_objects_v2')
            folders = set()
            for page in paginator.paginate(Bucket=settings.BUCKET_NAME, Delimiter='/'):
                for prefix in page.get('CommonPrefixes', []):
                    folders.add(prefix['Prefix'])
            return folders

        else:
            # fetch all the files path for the date range folders
            files = set()
            for folder in folders:
                response = self.s3_client.list_objects_v2(Bucket=settings.BUCKET_NAME, Prefix=folder)
                if 'Contents' in response:
                    for item in response['Contents']:
                        file_path = item['Key']
                        if not file_path.endswith('/'):  # Skip any subfolders
                            files.add(file_path)

            return list(files)

    def return_file_object(self, file):
        return self.s3_client.get_object(Bucket=settings.BUCKET_NAME, Key=file)
