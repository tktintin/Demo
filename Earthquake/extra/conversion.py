# converting csv file to python dictionary

import csv

dict = {}
file = 'countries.csv'
with open(file) as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        dict[row["name"]] = [row["latitude"] , row["longitude"]]
print(dict) 
# country : [latitude, longitude]