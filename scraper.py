# import search api
import googlesearch
search = googlesearch.search
search_news = googlesearch.search_news

from article import Article
from company import Company
from portfolio import Portfolio


class GoogleScraper:
    def __init__(self, portfolio = Portfolio(), start = "2019", end = "2019-09-20", max = 25):
        self.search_after = start
        self.search_before = end
        self.output_filename = 'out-' + start + "--" + end + ".txt"
        self.url_filename = 'urls.txt'
        self.max_articles_per_term = max
        
        self.portfolio = portfolio
    
        # create used_url list from file in portfolio
        #print("URLS already considered: ")
        self.used_urls = []
        try:
            up = open(self.portfolio.url_filename, "r")
            line = up.readline()
            while (line):
                self.used_urls.append(line.strip("\n"))
                #print(line)
                line = up.readline()
            up.close()
            print()
        except:
            print("no url file yet")
        
        #create articles list
        self.articles = []
    
    def scrape(self):
        # check out the company list and populate article list
        for cID in self.portfolio.companies:
            company = self.portfolio.companies[cID]
            print(company.name + ":", end = " ")
            for term in company.search_terms:
                print(term, end = ", ")
            print()
            
            print("Search Results for " + company.name + ": ")
            for term in company.search_terms:
                # call the google search news function and go through the urls
                for url in search_news(term + " after:" + self.search_after + " before:" + self.search_before, stop = self.max_articles_per_term): # we set it to get max articles per search term, between our two dates
                    url = url.strip(" ")
                    url = url.strip("\n")
                    print(url)
                    if not url in self.used_urls:
                        f = open(self.url_filename, "a")
                        print(url, file=f)
                        f.close()
                        self.used_urls.append(url)
                        print("URL saved to text file")
                        #check if url is blacklisted or should be considered
                        allow = True
                        for block in company.blacklist:
                            if block in url:
                                allow = False
                                print("URL was removed from consideration due to blacklist entry: " + block)
                                break
                        if allow:
                            this_article = Article(url)
                            this_article.parse() #parse it
                            this_article.output(self.output_filename) #output to files
                            self.articles.append(this_article)
                    else:
                        print("URL has already been considered.")
                    print()
                print()
