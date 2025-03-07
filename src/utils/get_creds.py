import boto3
import os
import base64

import sys, os
sys.path.append(os.path.abspath("src"))
sys.path.append('src') 

from src.utils.model_utils import get_latest_object_from_s3
def load_boto3_from_github_secrets(profile_name="default"):
    """
    Configures a Boto3 session using AWS credentials stored as GitHub secrets.

    Args:
        access_key_secret_name (str): The name of the GitHub secret containing the AWS access key ID.
        secret_key_secret_name (str): The name of the GitHub secret containing the AWS secret access key.
        region_secret_name(str): The name of the GitHub secret containing the aws region.
        profile_name (str, optional): The name of the Boto3 session profile. Defaults to "github_secrets_profile".

    Returns:
        boto3.Session: A configured Boto3 session.
    """

    try:
        # Retrieve secrets from environment variables (GitHub Actions)
        # access_key_id = os.environ.get('aws_access_key_id')
        # secret_access_key = os.environ.get('aws_secret_access_key')
        # region = os.environ.get('aws_region')
        
        # if not access_key_id or not secret_access_key or not region:
        #     raise ValueError("One or more AWS credential secrets are missing from the environment.")

        # Create a Boto3 session using the retrieved credentials
        session = boto3.Session(profile_name=profile_name)
        print(get_latest_object_from_s3(session=session,bucket_name='mlr-deployment-bucket', s3_prefix='test'))

        print("Boto3 session configured successfully from GitHub secrets.")
        return session

    except Exception as e:
        print(f"Error configuring Boto3 session: {e}")
        return None
    
print(load_boto3_from_github_secrets())
