import boto3
import io,os,sys
import pandas as pd
sys.path.append(os.path.abspath("src"))
sys.path.append(os.path.abspath("."))
from src.utils.get_creds import load_session

def save_predictions_to_s3(predictions, bucket_name, s3_key):
    """
    Saves predictions as a CSV file and uploads it to S3.

    Args:
        predictions (pd.Series): The predictions to save.
        bucket_name (str): The name of the S3 bucket.
        s3_key (str): The S3 key (path) for the CSV file.
    """
    try:
        # Create a DataFrame from the predictions
        predictions_df = pd.DataFrame({'predictions': predictions})

        # Save the DataFrame to a CSV string in memory
        csv_buffer = io.StringIO()
        predictions_df.to_csv(csv_buffer, index=False)
        csv_string = csv_buffer.getvalue()

        # Upload the CSV string to S3
        boto3 = load_session(local=True)
        s3 = boto3.client('s3')
        s3.put_object(Body=csv_string, Bucket=bucket_name, Key=s3_key)

        print(f"Predictions saved to s3://{bucket_name}/{s3_key}")

    except Exception as e:
        print(f"Error saving predictions to S3: {e}")