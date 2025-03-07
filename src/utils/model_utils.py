import joblib
import boto3
import os
import io
from datetime import datetime

def save_model_to_s3(model, bucket_name, s3_key,boto_session,temp_file_path="temp_model.joblib"):
    """
    Saves a trained machine learning model to an S3 bucket as a joblib file.

    Args:
        model: The trained machine learning model to save.
        bucket_name (str): The name of the S3 bucket.
        s3_key (str): The desired S3 key (path) for the saved model.
        boto_session (obj): The boto3 sesssion with the credentials.
        temp_file_path (str, optional): Local temporary file path for joblib. Defaults to "temp_model.joblib".
    """
    try:
        # Save the model to a temporary local file
        joblib.dump(model, temp_file_path)

        # Upload the file to S3
        s3 = boto_session.client('s3')
        s3.upload_file(temp_file_path, bucket_name, s3_key)

        print(f"Model saved to s3://{bucket_name}/{s3_key}")

    except Exception as e:
        print(f"Error saving model to S3: {e}")

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    pass


def get_latest_object_from_s3(session, bucket_name, s3_prefix):
    """
    Retrieves the latest (most recently modified) object from an S3 bucket with a given prefix.

    Args:
        session (boto3.Session): The Boto3 session to use for S3 operations.
        bucket_name (str): The name of the S3 bucket.
        s3_prefix (str): The S3 prefix (directory-like path).

    Returns:
        dict: The S3 object metadata (including 'Key') of the latest object, or None if no objects are found.
    """
    try:
        s3 = session.resource('s3')

        objects = list(s3.Bucket(bucket_name).objects.filter(Prefix=s3_prefix))
        objects.sort(key=lambda o: o.last_modified)
        print(objects[-1].key)
        return objects[-1].key

    except Exception as e:
        print(f"Error retrieving latest object: {e}")
        return None


def load_model_from_s3(session, bucket_name, s3_key):
    """
    Loads a machine learning model from an S3 bucket using a provided Boto3 session.

    Args:
        session (boto3.Session): The Boto3 session to use for S3 operations.
        bucket_name (str): The name of the S3 bucket.
        s3_key (str): The S3 key (path) of the model.

    Returns:
        object: The loaded machine learning model, or None if an error occurs.
    """
    obj = None
    try:
        s3 = session.client('s3')

        obj_name = get_latest_object_from_s3(session=session,bucket_name=bucket_name, s3_prefix=s3_key)
        assert obj_name != None
        obj = s3.get_object(Bucket=bucket_name, Key=f'{obj_name}')
        model_bytes = obj['Body'].read()
        model = joblib.load(io.BytesIO(model_bytes))
        print(f"Model loaded from s3://{bucket_name}/{s3_key}")
        return model

    except Exception as e:
        print(f"Error loading model from S3: {e}")
        return None

