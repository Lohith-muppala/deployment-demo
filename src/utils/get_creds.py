import boto3
import os
import base64

def load_boto3_from_github_secrets(access_key_secret_name, secret_key_secret_name, region_secret_name, profile_name="github_secrets_profile"):
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
        access_key_id = os.environ.get(access_key_secret_name)
        secret_access_key = os.environ.get(secret_key_secret_name)
        region = os.environ.get(region_secret_name)

        if not access_key_id or not secret_access_key or not region:
            raise ValueError("One or more AWS credential secrets are missing from the environment.")

        # Create a Boto3 session using the retrieved credentials
        session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region,
            profile_name=profile_name,
        )

        print("Boto3 session configured successfully from GitHub secrets.")
        return session

    except Exception as e:
        print(f"Error configuring Boto3 session: {e}")
        return None
