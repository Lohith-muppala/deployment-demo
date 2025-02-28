def load_data(path):
    import pandas as pd
    return pd.read_csv(path)

def transform(data):
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    le.fit(data.sex.drop_duplicates()) 
    data.sex = le.transform(data.sex)
    # smoker or not
    le.fit(data.smoker.drop_duplicates()) 
    data.smoker = le.transform(data.smoker)
    #region
    le.fit(data.region.drop_duplicates()) 
    data.region = le.transform(data.region)

    return data