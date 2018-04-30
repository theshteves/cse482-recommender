asins = set()

def create_dataset():
    fp2 = open('output.csv')
    fp = open('asin_img_lookup.csv')
    
    to_write = open('ratings.csv','w')
    
    #Copy over all user ratings
    for line in fp:
        asins.add(line.split(',')[0])
    
    found = 0
    not_found = 0
    for line in fp2:
        if line.split(',')[1] in asins:
            to_write.write(line)
            found += 1
        else:
            not_found += 1
            
    print(found, not_found)
        
    to_write.close()


create_dataset()













