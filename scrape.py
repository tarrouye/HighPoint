from scraper import GoogleScraper
from portfolio import Portfolio

goog = GoogleScraper(start = "2019-06-01", end = "2019-06-02")
goog.scrape()