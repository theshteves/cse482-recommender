import os
import csv

#Global dict for lookups
__ALL_ASIN = {}

def gen_dict():
    """
    Builds up the global dict, fills with ASIN keys and tuple values
    containing an image URL and product name
    """
    fp = open(os.path.join(os.path.dirname(__file__), 'asin_img_lookup.csv'))
    reader = csv.reader(fp)
    
    for line in reader:
        __ALL_ASIN[line[0]] = line
        
def asin_lookup(asin_list):
    """
    asin_list: list of ASIN values to lookup
    returns: List of lists containing (ASIN, imageURL, ProductName)
    """
    return_list = []
    for asin in asin_list:
        try:
            return_list.append(__ALL_ASIN[asin])
        except:
            print('ERROR: ASIN not found',asin)
            print('Product may not be in Home/Kitchen category?')
        
    return return_list
    
gen_dict()

#Example usage below
#query = asin_lookup(['0130350591','0587234792','0307394530'])
#print(query)
