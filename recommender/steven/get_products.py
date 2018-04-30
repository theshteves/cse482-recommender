import linecache
import random
import os

def get_products(datafile='output.csv', count=5, seed=-1):
    if seed != -1:
        random.seed(seed)

    with open(datafile, 'r') as data:
        num_lines = sum(1 for lines in data)

    # Grab 5 random product id's from first 1000 lines
    product_ids = set()
    while len(product_ids) < count:
        line_num = random.randint(1, num_lines - 2)
        line = linecache.getline(datafile, line_num)
        id_num = line.strip().split(',')[1]
        product_ids.add(id_num)

    return list(product_ids)
