from article import Article
import re

class ArticleReader:
    def __init__(self, file = 'out.txt'):
        self.articles = []
        self.parsed = False
        self.parse(file)
    
    def parse(self, file):
        f = open(file, "r")
        text = f.read()
        f.close()
        matches = re.findall("URL: (.*)\nParsed: (.*)\nAnalyzed: (.*)\nTitle: (.*)\nAuthor: (.*)\nBody: (.*)\n", text)
        
        for match in matches:
            self.articles.append(Article(match[0], match[1], match[2], match[3], match[4], match[5]))
        
        self.parsed = True
    