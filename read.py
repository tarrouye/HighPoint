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

from tkinter import *
from tkinter.ttk import *

# register matplotlib converters
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# -------------------------------- #
# ---------- Functions ----------- #
# -------------------------------- #


# function to plot the data from the selected files
def plot_data(article_file, percent_file, daily_file, line_type = '-'):
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
# ------ UI APP ----------------- #
# ------------------------------- #

class App:

    def __init__(self, master, alist, slist):
        # create a frame to hold our UI
        self.frame = Frame(master)
        self.frame.pack()
        
        style = Style()
        style.configure('TMenubutton', font = ('Futura', 14))
        style.configure('TButton', font = ('Futura', 16))
        style.configure('TCheckbutton', font = ('Futura', 16))
        style.configure('TLabel', font = ('Futura', 20, 'bold'))
        
        sm_font = ('Futura', 12)
        
        
        # create a variable to store the chosen article
        self.article = StringVar(self.frame)
        self.article.set(alist[0]) # default value

        # create a label for this selection
        self.article_label = Label(self.frame, text = "Article file: ", justify = LEFT, anchor = W)
        self.article_label.grid(row = 0, sticky = 'ew')

        # create a drop down menu of the article options
        self.article_menu = OptionMenu(self.frame, self.article, alist[0], *alist)
        self.article_menu['menu'].configure(font = sm_font)
        self.article_menu.grid(row = 0, column = 1, sticky = 'ew')
        
        
        def set_companies(*args):
            # ouput company choices
            self.df = pandas.read_csv(self.stock.get()).to_dict()
            
            clist = [ v for v in self.df['company'].values() ]
            
            # create a variable to store the chosen article
            self.company = StringVar(self.frame)
            self.company.set(clist[0]) # default value
    
            # create a label for this selection
            self.company_label = Label(self.frame, text = "Company: ", justify = LEFT, anchor = W)
            self.company_label.grid(row = 2, sticky = 'ew')
    
            # create a drop down menu of the company options
            self.company_menu = OptionMenu(self.frame, self.company, clist[0], *clist)
            self.company_menu['menu'].configure(font = sm_font)
            self.company_menu.grid(row = 2, column = 1, sticky = 'ew')
        
        
        # create a variable to store the chosen stock
        self.stock = StringVar(self.frame)
        self.stock.set(slist[0]) # default value
        self.stock.trace("w", set_companies)

        # create a label for this selection
        self.stock_label = Label(self.frame, text = "Stocks file: ", justify = LEFT, anchor = W)
        self.stock_label.grid(row = 1, sticky = 'ew')

        # create a drop down menu of the stock options
        self.stock_menu = OptionMenu(self.frame, self.stock, slist[0], *slist)
        self.stock_menu['menu'].configure(font = sm_font)
        self.stock_menu.grid(row = 1, column = 1, sticky = 'ew')
        
        # set default company choice
        set_companies()
        
        
        # create a variable to store the chosen plot style
        plist = ['-', 'o']
        
        self.plot = StringVar(self.frame)
        self.plot.set(plist[0]) # default value

        # create a label for this selection
        self.plot_label = Label(self.frame, text = "Plot style: ", justify = LEFT, anchor = W)
        self.plot_label.grid(row = 3, sticky = 'ew')

        # create a drop down menu of the stock options
        self.plot_menu = OptionMenu(self.frame, self.plot, plist[0], *plist)
        self.plot_menu['menu'].configure(font = sm_font)
        self.plot_menu.grid(row = 3, column = 1, sticky = 'ew')
        
        
        # create a button to confirm selections
        self.graph_button = Button(self.frame, text = "GRAPH", command = self.graph)
        self.graph_button.grid(row = 5, column = 1, sticky = 'ew', pady = 100)
        
        # create a button to quit the app
        self.quit_button = Button(self.frame, text = "QUIT", command = self.frame.quit)
        self.quit_button.grid(row = 5, column = 0, sticky = 'ew')
        

    def graph(self):
        article_file = self.article.get()
        company_index = [ v for v in self.df['company'].values() ].index(self.company.get())
        percent_file = self.df['percent file'][company_index]
        daily_file = self.df['daily file'][company_index]
        
        plot_data(article_file, percent_file, daily_file, self.plot.get())
    


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

root = Tk()
root.geometry("1000x500")

app = App(root, article_files, stock_files)

root.mainloop()