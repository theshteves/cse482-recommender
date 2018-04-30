import pandas as pd

"""
user values format:
    [
     [UserID, prodID, rating]
     [UserID, prodID, rating]
     ...
    ]
"""
def read_file(user_values=None, input_file='output.csv'):

    data_frame = pd.read_csv(input_file, header = 'infer', names = ['userID', 'prodID', 'rating'])
    

    user_data_frame = pd.DataFrame(user_values, columns = ['userID', 'prodID', 'rating'])
    data_frame = data_frame.append(user_data_frame, ignore_index = True)
    
    
    data_frame = data_frame.drop_duplicates(['userID', 'prodID'])
    data_frame = data_frame.fillna(0)
    
    
    data_frame2 = data_frame.pivot(columns='prodID', index='userID', values='rating')
    data_frame2 = data_frame2.fillna(0)

    return data_frame, data_frame2, user_values[0][0]
