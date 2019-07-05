from utility import articles_from_csv
from utility import stocks_from_csv

from scraper import StockScraper

import matplotlib.pyplot as plt
import pandas


# read in the Articles from the csv file
articles = articles_from_csv("out-idtsla-2016-01-01to2018-01-01.csv")

# read in our percent Stock data
stock_data_per = stocks_from_csv("out-percent-stock-idtsla-comp-Tesla-2016-01-01to2018-01-01.csv")

# read in our daily Stock data
stock_data_day = stocks_from_csv("out-daily-stock-idtsla-comp-Tesla-2016-01-01to2018-01-01.csv")

# populate a list with the contents of the article
data_list = []
for article in articles:
    dic = article.dictionary
    
    #we only care about the date not the time
    dic['publish-date'] = dic['publish-date'].date()
    
    data_list.append(dic)

# convert that list to a pandas Data Frame
df = pandas.DataFrame(data_list)

# sort the data by date
df.sort_values(by = 'publish-date', inplace = True)

grouped = df.groupby(by = 'publish-date')
mean = grouped.mean()
median = grouped.median()

# plot our data
line_type = '-'

plt.figure(2)

plt.plot(mean.index, mean['polarity'], 'b' + line_type, label='p_pos mean')
plt.plot(mean.index, mean['subjectivity'], 'r' + line_type, label='p_neg mean')
plt.legend(loc='upper left')

#plt.figure(2)

plt.plot(median.index, median['polarity'], 'c' + line_type, label='p_pos median')
plt.plot(median.index, median['subjectivity'], 'y' + line_type, label='p_neg median')
plt.legend(loc='upper left')

plt.figure(3)

plt.plot(stock_data_per['Close'], 'g' + line_type, label='(percent change)')
plt.legend(loc='upper left')

#plt.figure(4)

#plt.plot(stock_data_day['Close'], 'm-', label = 'closing price')
#plt.legend(loc='upper left')


plt.show()