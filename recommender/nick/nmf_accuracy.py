from surprise import Dataset
from surprise import Reader
from surprise import NMF
from surprise import accuracy
import random

def run_NMF(testset):
    reader = Reader(line_format='user item rating', sep=',')
    data = Dataset.load_from_file('train.csv',reader=reader)

    algo = NMF(n_factors=3, n_epochs=100, random_state=1)
    trainSet = data.build_full_trainset()
    algo.fit(trainSet)
    
    pred = algo.test(testset)

    return pred

def grab_reviews():
    test_reviews = []
    fp = open('ratings.csv')
    count = 0
    
    train = open('train.csv','w')
    
    for line in fp:
        if random.randint(1,11) == 5:
            count += 1
            line = line.split(',')
            line[2] = float(line[2].strip())
            #print(line)
            test_reviews.append(line)
            #rest_reviews.add(line.split(','))
        else:
            train.write(line)
    #print(test_reviews)
    print(count)
    train.close()
    return test_reviews
    
def test_nmf(nmf):
    return accuracy.rmse(nmf), accuracy.mae(nmf)

test_set = grab_reviews()
nmf = run_NMF(test_set)
print(test_nmf(nmf))


