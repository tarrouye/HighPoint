import csv
from datetime import datetime

class Article:
    def __init__(self, url = "", sentiment = None, polarity = None, subjectivity = None, title = "", pub = datetime.today(), access = datetime.today(), author = "", body = ""):
        self.dictionary = {
            'url': url,
            'title': title,
            'author': author,
            'publish-date': pub,
            'access-date': access,
            'body': body,
            'sentiment': sentiment,
            'polarity': polarity,
            'subjectivity': subjectivity
        }

    def __str__(self):
        return ("URL: " + self.dictionary['url'] +
            "\nSentiment: " + str(self.dictionary['sentiment']) +
            "\nPolarity: " + str(self.dictionary['polarity']) +
            "\nSubjectivity: " + str(self.dictionary['subjectivity']) +
            "\nTitle: " + self.dictionary['title'] +
            "\nPublish Date: " + str(self.dictionary['publish-date']) +
            "\nAccess Date: " + str(self.dictionary['access-date']) +
            "\nAuthor: " + self.dictionary['author'] +
            "\nBody: " + self.dictionary['body'])
    
    def output(self, fn):
        if (file_is_empty(fn)): # if the file is empty, we must add our csv header
            f = open(fn, "w")
            print("URL,Sentiment,Polarity,Subjectivity,Title,Published Date,Access Date,Author,Body", file=f)
            f.close()
        
        writeFile = open(fn, 'a', encoding='utf-8')
        csv.writer(writeFile).writerow([self.dictionary['url'], str(self.dictionary['sentiment']), str(self.dictionary['polarity']),
                str(self.dictionary['subjectivity']), self.dictionary['title'], self.dictionary['publish-date'], self.dictionary['access-date'], self.dictionary['author'], self.dictionary['body']])
                
        writeFile.close()
        print("Article saved to csv file: " + self.dictionary['title'])

# cyclical imports ;/
from utility import file_is_empty