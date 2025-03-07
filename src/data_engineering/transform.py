
from sklearn.preprocessing import PolynomialFeatures


import sys, os
sys.path.append(os.path.abspath("src"))
sys.path.append(os.path.abspath("."))
from src.data_engineering.etl import transform


def transform_features(data,mode = 'train'):
    if mode == 'train':
        data = transform(data)
        quad = PolynomialFeatures (degree = 2)
        X = data.drop(['charges','region'], axis = 1)
        y = data.charges
        X = quad.fit_transform(X)
        return X,y
    
    else:
        data = transform(data)
        quad = PolynomialFeatures(degree=2)
        X = data.drop(['charges','region'], axis = 1)
        y = data.charges
        X = quad.fit_transform(X)
        return X