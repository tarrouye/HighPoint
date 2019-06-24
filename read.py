from utility import articles_from_csv
from utility import stocks_from_csv

from portfolio import Portfolio
from scraper import StockScraper

import matplotlib.pyplot as plt
import pandas


# read in the Articles from the csv file
articles = articles_from_csv("out-idtsla-2016-01-01to2018-01-01.csv")

# read in our Stock data
stock_data = stocks_from_csv("out-stock-idtsla-comp-Tesla-2016-01-01to2018-01-01.csv")

# populate a list with the contents of the article
data_list = []
for article in articles:
    data_list.append(article.dictionary)

# convert that list to a pandas Data Frame
df = pandas.DataFrame(data_list)
# sort the data by date
df.sort_values(by = 'publish-date', inplace = True)

# plot our data
plt.figure(1)

plt.plot(df['publish-date'], df['polarity'], 'b-')
plt.plot(df['publish-date'], df['subjectivity'], 'r-')

plt.plot(stock_data['Close'] * 6, 'g-')
plt.show()