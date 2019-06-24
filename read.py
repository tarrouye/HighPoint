from articlereader import ArticleReader
import matplotlib.pyplot as plt
import pandas

reader = ArticleReader("out-idtsla-2019-06-01to2019-06-02.csv")

if reader.parsed:
    #data = pandas.DataFrame(columns = ['polarity', 'subjectivity', 'date'])
    for article in reader.articles:
        print(article)
        print("------------------------------")
        print()
    
