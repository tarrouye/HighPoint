from scraper import GoogleScraper
from portfolio import Portfolio

goog = GoogleScraper(start = "2019-06-17", end = "2019-06-18")
goog.scrape()