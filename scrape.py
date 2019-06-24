from scraper import GoogleScraper
from portfolio import Portfolio

# create a portfolio from the tesla file
tesla = Portfolio(company_file = "teslaonly.txt", id_ = 'tsla')

# run the google scraper
goog = GoogleScraper(tesla, start = "2016-01-01", end = "2018-01-01", max = 150)
goog.scrape()

# run the stock scraper on the same time frame
stock = StockScraper(tesla, start = "2016-01-01", end = "2018-01-01")
stock.scrape()