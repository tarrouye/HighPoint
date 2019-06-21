from scraper import GoogleScraper

goog = GoogleScraper("companies.txt", "2019-06-17", "2019-06-18")
goog.scrape()