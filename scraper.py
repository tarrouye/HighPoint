######## scraper.py ########

######## GoogleScraper ########
import googlesearch
search = googlesearch.search
search_news = googlesearch.search_news

import requests

from bs4 import BeautifulSoup

from textblob import TextBlob

from newspaper import Article as NewsArticle
import nltk
nltk.download("punkt")

from datetime import datetime

import csv

from utility import str_to_datetime
from utility import file_is_empty

import articleDateExtractor as getdate

from article import Article
from company import Company
from portfolio import Portfolio

err_file = "err.csv"

class GoogleScraper:
    def __init__(self, portfolio = Portfolio(), start = "2019", end = "2019-09-20", max = 25):
        #setting our initial variables
        self.search_after = start # the start of the time period to scrape
        self.search_before = end # the end of the time period to scrape
        self.output_filename = 'out-id' + portfolio.id + "-" + start + "to" + end + ".csv" #wack filename sorry
        self.max_articles_per_term = max # how many articles to scrape per search term
        
        self.portfolio = portfolio # the portfolio to
    
        # create used_url list from file in portfolio
        self.used_urls = []
        try:
            up = open(self.portfolio.url_filename, "r") # open the file
            line = up.readline()
            while (line): # go through each line, get the url, and add it to the list
                self.used_urls.append(line.strip("\n"))
                line = up.readline()
            up.close()
            print()
        except:
            print("no url file yet")
        
        #create articles list
        self.articles = []
    
    def scrape(self):
        # go through company list to scrape their search terms
        for cID in self.portfolio.companies:
            company = self.portfolio.companies[cID]
            
            print("Search Results for " + company.name + ": ")
            
            for term in company.search_terms: # go through each search term
                # call the google search news function and go through the urls it returns
                for url in search_news(term + " after:" + self.search_after + " before:" + self.search_before, stop = self.max_articles_per_term): # we set it to get max articles per search term, between our two dates
                    url = url.strip(" ")
                    url = url.strip("\n") #remove extraneous leading/trailing characters in the url
                    
                    print(url)
                    
                    if not url in self.used_urls: # we don't want to waste time looking at urls we've already dealt with
                        f = open(self.portfolio.url_filename, "a")
                        print(url, file=f) #add this url to the list of dealt with
                        f.close()          #as well as to the file
                        self.used_urls.append(url)
                        
                        print("URL saved to text file")
                        
                        #check if url is blacklisted or should be considered
                        allow = True
                        for block in company.blacklist:
                            if block in url:   # run through company's url blacklist to see if this url
                                allow = False  # is in it, in which case we end here
                                print("URL was removed from consideration due to blacklist entry: " + block)
                                break
                            
                        if allow: # if not blacklisted url, we move to parse this URL
                            self.parseURL(url)
                    else:
                        print("URL has already been considered.")
                        
                    print()
                print()
                
    def parseURL(self, url):
        # create Newspaper3k object
        news3 = NewsArticle(url)

        # download and parse the article
        try:
            news3.download()
            news3.parse()
        except:
            self.logerror(url, "Download Failed") # protect from failure with a try except
            return
        
        # check date / end
        pub = news3.publish_date # try to get the date from Newspaper3k
        access = datetime.today() # we accessed this rn
        
        # second date attempt if first failed
        if (pub == None):
            pub = getdate.extractArticlePublishedDate(url)
            
        # we need the date so if we cant find it we simply throw this article away
        if (pub == None):
            self.logerror(url, "Date Detection Failed - Missing")
            return
        
        # sometimes the date thing gets the wrong date - WACK
        # but to be smart we'll throw anything out that is outside
        # of our search range and pray to Jesus that the rest are accurate
        pub = str_to_datetime(pub)
        if (pub < str_to_datetime(self.search_after) or pub > str_to_datetime(self.search_before)):
            self.logerror(url, "Date Detection Failed - Out of Bounds")
            return
        
        # TextBlob Analysis
        textBlobObj = TextBlob(news3.text) # create textBlob object
        
        # language / end
        try:
            lang = textBlobObj.detect_language()
            if (lang != 'en'):
                self.logerror(url, "Non English Article")
                return # we only want to deal with English articles
        except:
            self.logerror(url, "Language Detection Failed")
            return
            
        # have TextBlob calculate sentiment
        try:
            sentiment = textBlobObj.sentiment
        except:
            self.logerror(url, "Sentiment Analysis Failed")
            return
        
        # Add to article list
        this_article = Article(url, sentiment, sentiment.polarity, sentiment.subjectivity, news3.title, pub, access, ' + '.join(news3.authors), news3.text)
        this_article.output(self.output_filename) #output to files
        self.articles.append(this_article) # add to our list
        
    def logerror(self, url, error):
        if (file_is_empty(err_file)): # if the file is empty, we must add our csv header
            f = open(err_file, "w")
            print("URL,Error", file=f)
            f.close()
        
        writeFile = open(err_file, 'a', encoding='utf-8')
        csv.writer(writeFile).writerow([url, error])
        
        writeFile.close()
        
        print(error + " logged in error file.")



######## StockScraper ########
import matplotlib.pyplot as plt
import quandl
import pandas

class StockScraper:
    def __init__(self, portfolio = Portfolio(), start = "2016-01-01", end = "2018-01-01"):
        self.search_after = start
        self.search_before = end
        self.portfolio = portfolio
        self.output_filename = 'out-stock-id' + portfolio.id + "-" + start + "to" + end + ".csv"
    
    def scrape(self):
        data_frame = pandas.DataFrame()
        
        # check out the company list and populate stock list
        for cID in self.portfolio.companies:
            company = self.portfolio.companies[cID]
            
            #get daily stock data from Quandl
            data = quandl.get(company.stock_symbol, start_date = self.search_after, end_date = self.search_before)
            
            #get percentage change stock data from Quandl
            data2 = quandl.get(company.stock_symbol, transform="rdiff", start_date = self.search_after, end_date = self.search_before)
            
            #create output filenames for this portfolio/company/date combo
            comp_out = 'out-daily-stock-id' + self.portfolio.id + "-comp-" + company.name + "-" + self.search_after + "to" + self.search_before + ".csv"
            comp_out_2 = 'out-percent-stock-id' + self.portfolio.id + "-comp-" + company.name + "-" + self.search_after + "to" + self.search_before + ".csv"
            
            #export stock data to csv file
            export = data.to_csv(comp_out, header = True)
            export2 = data2.to_csv(comp_out_2, header = True)
            print("Saved stock data for " + company.name + " to csv file.")
            
            #add this file to our data_frame
            df2 = {'company': company.name, 'daily file': comp_out, 'percent file': comp_out_2}
            data_frame = data_frame.append(df2, ignore_index=True)
        
        #export list of csv files to main portfolio/date csv file
        data_frame.to_csv(self.output_filename, header = True, index = None)
        print("Saved csv files for " + self.portfolio.id + " to main output file.")
