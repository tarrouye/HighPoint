from article import Article
import re
import csv

class ArticleReader:
    def __init__(self, file = 'out.csv'):
        self.articles = []
        self.parsed = False
        self.parse(file)
        
    def parse(self, file):
        try:
            readFile = open(file, 'r')
        except:
            print("Invalid file passed to ArticleReader.")
            return
        
        
        for match in csv.reader(readFile):
            self.articles.append(Article(match[0], match[1], match[2], match[3], match[4], match[5], match[6], match[7], match[8]))
        
        readFile.close()
        self.parsed = True
    