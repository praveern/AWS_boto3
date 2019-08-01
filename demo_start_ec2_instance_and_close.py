"""
This script is for opening an EC2 instance and uploading some documents to S3 as a new bucket.
It will also eventually close the EC2 instance. There will be a function to restart it if needed.

"""

import os
import sys
import boto3
import random

sys.path.append(os.getcwd())


class CreateThumbnail:
    """
    Lambda function class
    """
    def __init__(self, lambda_function_name, region, ):
        self.__ZIPS_LOCATION = os.path.join(os.getcwd(), "zips", "CreateThumbnail")
        if not os.path.exists(self.__ZIPS_LOCATION):
            os.makedirs(self.__ZIPS_LOCATION)

    # Lambda Handler

    # Lambda Trigger setup (with SNS/CloudWatch)

    # Lambda zip creator


# Bucket setup for resources/lambdas
def create_s3_buckets(current_session, bucket_name, region_to_create_in, is_it_lambda_function=False):
    """
    Creates a S3 bucket for the session and using the provided bucket name in the selected region.
    The flow depends on whether the S3 bucket is supposed to be deployed for lambda function or
    resources.

    :param current_session: Current session.
    :param bucket_name: Name of the bucket to be created.
    :param region_to_create_in: Region where to create and save the bucket.
    :param is_it_lambda_function: Boolean, controls the flow. Default False.
    :return: Nothing.
    """
    # Initiate S3 client
    def_s3_client = current_session.client('s3')

    if not is_it_lambda_function:
        # Input
        def_s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration={'LocationConstraint': region_to_create_in})
        newdata = open("C:\\Users\\Praveer\\Pictures\\Saved Pictures\\League Wallpapers\\Classic-Ryze.jpg", "rb")
        def_s3_client.put_object(Bucket=bucket_name, Key="Classic-Ryze.jpg", Body=newdata)
        newdata.close()

        # Output
        new_bucket_name = bucket_name+"-resized"
        def_s3_client.create_bucket(Bucket=new_bucket_name,
                                    CreateBucketConfiguration={'LocationConstraint': region_to_create_in})
    else:
        # Store lambda function zip
        def_s3_client.create_bucket(Bucket=bucket_name+"-create-thumbnail",
                                    CreateBucketConfiguration={'LocationConstraint': region_to_create_in})


if __name__ == '__main__':
    # Create session
    session = boto3.Session(profile_name="default")

    # Generate random number for creating bucket name
    xr = random.randint(10000000000, 100000000000000000)
    common_part = "image-" + str(xr)

    # Generate buckets for resources:
    create_s3_buckets(session, common_part, "us-west-1")

    # Generate bucket for Lambda function:
    create_s3_buckets(session, common_part, "us-west-1", is_it_lambda_function=True)

    # Create the lambda function zip file to be uploaded to the S3 bucket.
    new_ct = CreateThumbnail(lambda_function_name="CreateThumbnail", region="us-west-1",)
