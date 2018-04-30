import nmfalgo
import asin_lookup

#Below is simulated review data, we will collect this data from the user
rev = [['Nick','B00002N602','3'],['Nick','B003QI9HPW','5'],
       ['Nick','B003QX2JMA','1']]

#Run our NMF algo and get the results
results = nmfalgo.run_NMF(rev,'Nick',10)

#Build a list of only the reccomended ASIN numbers
asins = []
for item in results:
    asins.append(item[1])

#Use asin_lookup function to get a list of product names, img urls, and asin
names = asin_lookup.asin_lookup(asins)

#Print out our top products
print('Product Suggestions')
print('-----------------------')
for i,n in enumerate(names):
    print(i+1,'. ',n[2])
    