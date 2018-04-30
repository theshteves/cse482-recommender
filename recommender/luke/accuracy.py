import pandas as pd
from sklearn.metrics import pairwise 
from operator import itemgetter
import numpy as np
#import math

"""
READ ME
This file contains modified filtering functions specifically changed to help 
test accuracy in a consistent way. These functions are only to be used with
the accuracy function
"""


"""
user values format:
    [
     [UserID, prodID, rating]
     [UserID, prodID, rating]
     ...
    ]
"""
def read_file(user_values=None):

    data_frame = pd.read_csv("output.csv", header = 'infer', names = ['userID', 'prodID', 'rating'])
    
    
    #data_frame = data_frame.tail(int(math.sqrt(data_frame.size)))

    
    user_data_frame = pd.DataFrame(user_values, columns = ['userID', 'prodID', 'rating'])
    data_frame = data_frame.append(user_data_frame, ignore_index = True)

    
    data_frame = data_frame.drop_duplicates(['userID', 'prodID'])
    data_frame = data_frame.fillna(0)
    
    
    data_frame2 = data_frame.pivot(columns='prodID', index='userID', values='rating')
    data_frame2 = data_frame2.fillna(0)
    
    if user_values:
        return data_frame, data_frame2, user_values[0][0]
    else:
        return data_frame, data_frame2, None



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
        if data_frame[data_frame.columns[i]][user_ID] == 0:
            predictions.append((item, predicted))
        
    predictions.sort(key=itemgetter(1), reverse=True)
    final_predictions = [i for i in predictions if i[1] == 5]
    return(final_predictions)


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
    max_score = max([i[1] for i in predictions])
    final_predictions = [i for i in predictions if i[1] == max_score]
    return(final_predictions)

  

def accuracy():
    df, df2, user_ID = read_file()
    users = [i for i in df2.index]
    
    total = 0
    count = 0
    for i in range(3*len(users)/4, len(users)):
        total += 1
        masked = max(df2.iloc[i].nonzero())
        masked = masked[0]
        secret_rating = df2[df2.columns[masked]][users[i]]
        secret_item = df2.columns[masked]
        df2[df2.columns[masked]][users[i]] = 0
        temp = []
        temp1 = []

        temp1 = collab_by_user(df, df2, users[i])
        for item in temp1:
            temp.append(item[0])
        if secret_item in temp:
            count += 1
        df2[df2.columns[masked]][users[i]] = secret_rating
            
    accuracy = count / total
    print("user-based accuracy:", accuracy)

    total = 0
    count = 0
    for i in range(3*len(users)/4, len(users)):
        total += 1
        masked = max(df2.iloc[i].nonzero())
        masked = masked[0]
        secret_rating = df2[df2.columns[masked]][users[i]]
        secret_item = df2.columns[masked]
        df2[df2.columns[masked]][users[i]] = 0
        temp = []
        temp1 = []

        temp1 = collab_by_item(df, df2, users[i])
        for item in temp1:
            temp.append(item[0])
        if secret_item in temp:
            count += 1
        df2[df2.columns[masked]][users[i]] = secret_rating
            
    accuracy = count / total
    print("item-based accuracy:", accuracy)

accuracy()