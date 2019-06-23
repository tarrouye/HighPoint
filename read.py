from articlereader import ArticleReader

reader = ArticleReader("out-idp0001-2019-06-01to2019-06-02.csv")

if reader.parsed:
    for article in reader.articles:
        print(article)
        print("------------------------------")
        print()
    
