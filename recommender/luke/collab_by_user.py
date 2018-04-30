import pandas as pd
from sklearn.metrics import pairwise 
from operator import itemgetter
import numpy as np

def collab_by_user(data_frameAlpha, data_frame, user_ID):

    products = [i for i in data_frame.columns]

    X = data_frame.as_matrix()
    user_similarity = pairwise.rbf_kernel(X[:,:3],gamma=0.2)
    usim = pd.DataFrame(user_similarity)
    
    data_frame_nan = data_frame.replace(0, np.NaN)
    avg_ratings = data_frame_nan.mean(axis=1)
    
    predictions = []
    for i, item in enumerate(products):
        ratings = (data_frame[item][:i+1:] - avg_ratings[:i+1:])*usim[i].loc[:i+1:]
        predicted = avg_ratings[i] + (ratings.sum()*1.0/usim[i].loc[i+1:].sum())
        predictions.append((item, predicted))
        
    predictions.sort(key=itemgetter(1), reverse=True)
    return(predictions[:3])
