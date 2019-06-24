from scraper import GoogleScraper
from portfolio import Portfolio

tesla = Portfolio(company_file = "teslaonly.txt", id_ = 'tsla')

goog = GoogleScraper(tesla, start = "2019-06-01", end = "2019-06-02")
goog.scrape()