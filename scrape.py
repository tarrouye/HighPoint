from scraper import GoogleScraper
from portfolio import Portfolio

goog = GoogleScraper(start = "2018-10-22", end = "2018-10-29")
goog.scrape()