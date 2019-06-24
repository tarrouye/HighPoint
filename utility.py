########                     utility.py                          ########
######## useful functions which shouldn't belong to any one class ########


import pandas
from datetime import datetime

import re
import csv

# takes the filename of a csv file of Articles and converts
# it to a list which it returns
def articles_from_csv(file):
    try:
        readFile = open(file, 'r')
    except:
        print("Invalid file passed to Article reader.") # try except block protects against invalid filenames
        return
    
    articles = [] # list to hold the Articles
    
    csvreader = csv.reader(readFile) # create a cvs reader object
    
    next(csvreader) # skip the header
    for match in csvreader: # go through each row of the cvs file
        pub = str_to_datetime(match[5]) # convert the dates back to datetime
        acc = str_to_datetime(match[6])
        # create the Article and add it to the list
        articles.append(Article(match[0], match[1], float(match[2]), float(match[3]), match[4], pub, acc, match[7], match[8]))
    
    readFile.close() # close the file ;)
    
    return articles
    
# takes the filename of a csv file of stock data and converts
# it to a pandas DataFrame which it returns
def stocks_from_csv(file):
    try:
        readFile = open(file, 'r')
    except:
        print("Invalid file passed to stocks csv reader.") # try except block protects against invalid filenames
        return
    
    # we set it to parse the date in the index column and read in from file
    stocks = pandas.read_csv(file, index_col = 0, parse_dates = True, infer_datetime_format = True)
    
    return stocks


# converts a date string to a datetime object using pandas
def str_to_datetime(str_):
    return pandas.to_datetime(str_, infer_datetime_format = True, errors = 'coerce').tz_localize(None)
    
    
# determines whether a file exists or not
# using a simple try-except block
def file_is_empty(path):
    try:
        f = open(path, "r")
        f.close()
        return False
    except:
        return True
        
        
        
# cyclical imports ;/
from article import Article