# -------------------------------- #
# ----------- Imports ------------ #
# -------------------------------- #

from utility import articles_from_csv
from utility import stocks_from_csv

import matplotlib.pyplot as plt
import pandas

import os
from os import listdir
import sys

# -------------------------------- #
# ---------- Functions ----------- #
# -------------------------------- #

# function to output list of files and
# return the one the user selects
def select_file(flist, id_):
    print("File choices: ")
    
    # output file choices
    count = 0
    for file_name in flist:
        print(str(count) + ": " + file_name)
        count += 1
            
    # loop asking for them to pick one
    loop2 = True
    while (loop2):
        ask = input("Select your " + id_ + " File: ")
        try:
            num = int(ask)
            file1 = flist[num]
            loop2 = False
        except:
            print("Invalid input. ")
    
    print()
    print("-------------------------")
    print()

    return file1
    
# function to output list of companies in stock file
# and return the files for the one the user selects
def select_company(cfile):
    print("Company choices: ")
    
    # ouput company choices
    df = pandas.read_csv(cfile).to_dict()
    
    for id_ in df['company']:
        print(str(id_) + ": " + df['company'][id_])
    
    # loop asking for them to pick one
    loop2 = True
    while (loop2):
        ask = input("Select a company: ")
        try:
            num = int(ask)
            file1 = df['percent file'][num]
            file2 = df['daily file'][num]
            loop2 = False
        except:
            print("Invalid input. ")
    
    print()
    print("--------------------------")
    print()
    
    return file1, file2


# function to plot the data from the selected files
def plot_data(article_file, percent_file, daily_file):
    # read in the Articles from the csv file
    articles = articles_from_csv(article_file)
    
    # read in our percent Stock data
    stock_data_per = stocks_from_csv(percent_file)
    
    # read in our daily Stock data
    stock_data_day = stocks_from_csv(daily_file)
    
    # populate a list with the contents of the article
    data_list = []
    for article in articles:
        dic = article.dictionary
        
        #we only care about the date not the time
        dic['publish-date'] = dic['publish-date'].date()
        
        data_list.append(dic)
    
    # convert that list to a pandas Data Frame
    df = pandas.DataFrame(data_list)
    
    # sort the data by date
    df.sort_values(by = 'publish-date', inplace = True)
    
    grouped = df.groupby(by = 'publish-date')
    mean = grouped.mean()
    median = grouped.median()
    
    # plot our data
    line_type = '-'
    
    plt.figure(1)
    
    plt.plot(mean.index, mean['polarity'], 'b' + line_type, label='p_pos mean')
    plt.plot(mean.index, mean['subjectivity'], 'r' + line_type, label='p_neg mean')
    plt.legend(loc='upper left')
    
    plt.figure(2)
    
    plt.plot(median.index, median['polarity'], 'c' + line_type, label='p_pos median')
    plt.plot(median.index, median['subjectivity'], 'y' + line_type, label='p_neg median')
    plt.legend(loc='upper left')
    
    plt.figure(3)
    
    plt.plot(stock_data_per['Close'], 'g' + line_type, label='(percent change)')
    plt.legend(loc='upper left')
    
    plt.figure(4)
    
    plt.plot(stock_data_day['Close'], 'm' + line_type, label = 'closing price')
    plt.legend(loc='upper left')
    
    
    plt.show()
    
    
    
# ------------------------------- #
# ----------- Script ------------ #
# ------------------------------- #

# get the path to the directory this file is in
# we assume output files will be here.
current_path = os.path.dirname(os.path.realpath(__file__)) + "/"

# create lists to hold files we find
article_files = []
stock_files = []

# find output files
for file_name in listdir(current_path):
    if (('out-stock' in file_name) and file_name.endswith('.csv')): # we look for specific stock files from our output
        stock_files.append(file_name)
        
    if (('out-id' in file_name) and file_name.endswith('.csv')): # we look for specific article files from our output
        article_files.append(file_name)
        
        
# have user select article and stock files
a_file = select_file(article_files, "Article")
s_file = select_file(stock_files, "Stock")

# read in the stock file
p_file, d_file = select_company(s_file)

print("You have selected to analyze the following files: ")
print("Article file: " + a_file)
print("Percent change file: " + p_file)
print("Daily price file: " + d_file)
print()
print("------------------")
print()
print("Graphing now")
plot_data(a_file, p_file, d_file)
    
print("Exiting reader.")
print()