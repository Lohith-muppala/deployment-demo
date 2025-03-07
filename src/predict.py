import sys,os
sys.path.append(os.path.abspath("src"))
sys.path.append(os.path.abspath("."))

from src.modeling.LinearRegressor import LR_Model
from src.utils.get_creds import load_session
from src.utils.model_utils import load_model_from_s3
from src.utils.prediction_upload import save_predictions_to_s3
from src.data_engineering.transform import transform_features
import pandas as pd
from datetime import datetime
import joblib



def main():
    """
    Loads a trained LR_Model and makes predictions on new data.

    Args:
        data (pd.DataFrame): The input data for prediction.
        model_path (str, optional): Path to the saved model file. Defaults to "model.joblib".

    Returns:
        pd.Series: The predicted values.
    """
    try:
        # Load the model
        session = load_session(local=True)
        model = load_model_from_s3(session,bucket_name='mlr-deployment-bucket',s3_key='models')
        data = pd.read_csv('data\insurance.csv')
        # Create a dummy LR_Model instance to use its methods.
        dummy_model = LR_Model(data)
        dummy_model.model = model #set the loaded model to the dummy model.

        # Transform the features (same preprocessing as during training)
        X =transform_features(data, mode='inference')
        # Make predictions
        predictions = dummy_model.predict(X)
        save_predictions_to_s3(predictions=predictions,bucket_name='mlr-deployment-bucket',s3_key=f'predictions/{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.csv')

        return pd.Series(predictions)

    except FileNotFoundError:
        print(f"Error: Model file not found.")
        return None
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return None
    
if __name__ == "__main__":
    main()

