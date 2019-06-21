from articlereader import ArticleReader

reader = ArticleReader()

if reader.parsed:
    for article in reader.articles:
        print(article)
        print("------------------------------")
        print()
    
