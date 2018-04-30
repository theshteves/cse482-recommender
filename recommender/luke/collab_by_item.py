import pandas as pd
from sklearn.metrics import pairwise 
from operator import itemgetter

def collab_by_item(data_frameAlpha, data_frame, user_ID):
    

    users = [i for i in data_frame.index]

    
    X = data_frame.as_matrix()
    item_similarity = pairwise.rbf_kernel(X[1:,:].T,gamma=0.2)
    isim = pd.DataFrame(item_similarity)
    
    predictions = []
    for i, item in enumerate(users):
        ratings = data_frame.loc[user_ID][:i:].as_matrix()
        if i >= len(isim):
            continue
        simval = isim[i][:i:]
        if simval.sum() != 0:
            prediction = (simval*ratings).sum()/simval.sum()
            if data_frame[data_frame.columns[i]][user_ID] == 0:
                predictions.append((data_frame.columns[i], prediction))
        
    predictions.sort(key=itemgetter(1), reverse=True)
    return(predictions[:3])