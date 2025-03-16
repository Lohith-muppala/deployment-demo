import boto3
import os
import base64

import sys, os
sys.path.append(os.path.abspath("src"))

from utils.model_utils import get_latest_object_from_s3

def load_session(profile_name="default",local=False):
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
    if not local:
        # try:
        sts_client = boto3.client('sts')

        # Call the assume_role method of the STSConnection object and pass the role
        # ARN and a role session name.
        assumed_role_object=sts_client.assume_role(
            RoleArn="arn:aws:iam::897729134151:role/github-actions",
            RoleSessionName="AssumeRoleSession1"
        )

        credentials=assumed_role_object['Credentials']
        
        access_key_id=credentials['AccessKeyId']
        secret_access_key=credentials['SecretAccessKey']
        session_token=credentials['SessionToken']

        print(access_key_id)
        
        if not access_key_id or not secret_access_key :
            raise ValueError("One or more AWS credential secrets are missing from the environment.")

        # Create a Boto3 session using the retrieved credentials
        session = boto3.Session(aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key,aws_session_token = session_token)
        print("Boto3 session configured successfully from GitHub secrets.")
        return session

        # except Exception as e:
        #     print(f"Error configuring Boto3 session with key and secret: {e}")
        #     return None
    else:
        try:
            # Create a Boto3 session using the retrieved credentials
            session = boto3.Session(profile_name=profile_name)
            print("Boto3 session configured successfully from GitHub secrets.")
            return session

        except Exception as e:
            print(f"Error configuring Boto3 session: {e}")
            return None
    

