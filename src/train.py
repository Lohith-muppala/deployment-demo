import sys,os
sys.path.append(os.path.abspath("./app/src"))
sys.path.append(os.path.abspath("/src"))
sys.path.append(os.path.abspath("."))


from src.data_engineering.transform import transform_features
from src.modeling.LinearRegressor import LR_Model
from src.utils.get_creds import load_session
from src.utils.model_utils import save_model_to_s3
import pandas as pd
from datetime import datetime



def main():
    # Load your dataset (replace 'insurance.csv' with your actual file path)
    data = pd.read_csv('./data/insurance.csv')

    # Create an instance of the LR_Model
    model = LR_Model(data)

    # Transform features
    X, y = transform_features(data, mode='train')

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = model.split_data(X, y)

    # Fit the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    model.score(y_pred, y_test)

    #save model
    session = load_session(local=False)
    print('Saving model...')
    save_model_to_s3(model,bucket_name='mlr-deployment-bucket',s3_key=f'models/{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.joblib',boto_session=session)
    print(f'Saved model:models/{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}')
if __name__ == "__main__":
    main()