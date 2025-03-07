from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score,mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from src.data_engineering.etl import transform

class LR_Model:

    def __init__(self,data,test_size=0.2,random_state=42):
        self.data = data
        self.model = None
        self.mode = None
        self.test_size = test_size
        self.random_state = random_state
    
    def split_data(self,X,y):
        X_train,X_test,Y_train,Y_test = train_test_split(X,y,test_size=self.test_size,random_state = self.random_state)
        return X_train,X_test,Y_train,Y_test
    
    def fit(self,X,y):
        model = LinearRegression().fit(X,y)
        self.model = model
        return model

    def transform_features(self,data,mode = 'train'):
        if mode == 'train':
            self.mode = 'train'
            data = transform(data)
            self.data = data
            quad = PolynomialFeatures (degree = 2)
            X = data.drop(['charges','region'], axis = 1)
            y = data.charges
            X = quad.fit_transform(X)
            return X,y
        
        else:
            self.mode = 'inference'
            quad = PolynomialFeatures(degree=2)
            X = quad.fit_transform(X)
            return X

    def predict(self,data):
        assert self.model != None, 'Model empty or not fitted!'
        Y_test_pred = self.model.predict(data)
        return Y_test_pred
    
    def score(self,predictions,actuals):
        print('MSE test data: %.3f' % (
        mean_squared_error(actuals,predictions)))
        print('R2 test data: %.3f' % (
        r2_score(actuals,predictions)))
        return mean_squared_error(actuals,predictions), r2_score(actuals,predictions)

        