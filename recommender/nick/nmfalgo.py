import os

from surprise import Dataset
from surprise import Reader
from surprise import NMF

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
__ALL_ASIN = set()

def create_dataset(user_ratings):
    """
    user_ratings: list of lists containing ratings created by the user of site
    This function builds up a temporary dataset and appends the users ratings
    to the end of the dataset (the reason for this is that we need to build
    a matrix of data and include the user ratings in the entire dataset to
    build a proper matrix)
    """
    fp = open(os.path.join(THIS_DIR, 'output.csv'), 'r')
    to_write = open(os.path.join(THIS_DIR, 'temp_dataset_incl_usr_reviews.csv'),'w')
    
    #Copy over all user ratings
    for line in fp:
        __ALL_ASIN.add(line.split(',')[1])
        to_write.write(line)
    #Add in the new ratings created by user of out site
    for list_item in user_ratings:
        to_add = ','.join(str(joiner) for joiner in list_item)
        #Writing a line to temp file and adding a newline
        to_write.write(to_add+'\n')
        
    to_write.close()

def build_NMF(user_name):
    """
    Builds the NMF from the data file we constructed
    """
    reader = Reader(line_format='user item rating', sep=',')
    data = Dataset.load_from_file(os.path.join(THIS_DIR, 'temp_dataset_incl_usr_reviews.csv'),
                                  reader=reader)


    algo = NMF(n_factors=3, n_epochs=100, random_state=1)
    trainSet = data.build_full_trainset()
    algo.fit(trainSet)
    
    
    #Generate testset from all ASINS
    testset = []
    for asin in __ALL_ASIN:
        testset.append([user_name,asin,0])
    
    
    
    
    pred = algo.test(testset)
    
    rec = []
    
    for (uid,iid,r_ui,est,details) in pred:
        #print('(%s, %s): predicted = %.2f (true = %.2f)' %
        #      (uid, iid, est, r_ui))
        rec.append((est,iid))
    rec.sort(reverse=True)
    return rec
        
        
def run_NMF(usr_reviews,user_name,num_recs):
    """
    usr_reviews: list of lists containing [user, ASIN, rating]
    """
    create_dataset(usr_reviews)
    return build_NMF(user_name)[:num_recs]


#EXAMPLE USAGE BELOW
#
#example_usr_reviews = [['Nick','B00002N602','3'],['Nick','B003QI9HPW','5'],
#                       ['Nick','B003QX2JMA','1']]
#num_of_recs = 10
#reccomendations = run_NMF(example_usr_reviews,'Nick',num_of_recs)
#print(reccomendations)
#
#















