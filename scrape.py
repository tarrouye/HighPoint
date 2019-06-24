from scraper import GoogleScraper
from scraper import StockScraper
from portfolio import Portfolio

# create a portfolio from the tesla file
tesla = Portfolio(company_file = "teslaonly.csv", id_ = 'tsla')

# run the stock scraper
stock = StockScraper(tesla, start = "2016-01-01", end = "2018-01-01")
stock.scrape()

# run the google scraper on the same time frame
goog = GoogleScraper(tesla, start = "2016-01-01", end = "2018-01-01", max = 150)
goog.scrape()

