import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import csv

err_file = "err.txt"

class Article:
    def __init__(self, url = "", parsed = False, analyzed = False, sentiment = None, polarity = None, subjectivity = None, title = "", author = "", body = ""):
        self.dictionary = {
            'url': url,
            'title': title,
            'author': author,
            'body': body,
            'parsed': parsed,
            'analyzed': analyzed,
            'sentiment': sentiment,
            'polarity': polarity,
            'subjectivity': subjectivity
        }

    def parse(self):
        paragraphtext = []
        # get page text and parse with BFS
        print("requesting page")
        # catch timeout errors and other request exceptions
        try:
            page = requests.get(self.dictionary['url'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        except requests.exceptions.RequestException as e:
            self.logerror(str(e))
            return
        
        # catch 404 errors
        if page.status_code == 404:
            self.logerror("404 On Request")
            return
            
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # get author name, if there's a named author
        # currently works on MarketWatch
        try:
            abody = soup.find(class_='byline').find('a')
            aname = abody.get_text()
        except:
            aname = 'Anonymous'
            
        self.dictionary['author'] = aname.strip("\n").strip(" ").strip("\t")
        
        # get article title or log error
        try:
            title = soup.title.get_text()
        except:
            title = ""
            self.logerror("Title Not Found")
            
        self.dictionary['title'] = title.strip("\n").strip(" ").strip("\t")
        
        # get article text
        try:
            articletext = soup.find(id='article-body').find_all('p')
        except:
            try:
                articletext = soup.find(class_='story-body').find_all('p')
            except:
                print("Could not narrow down body location")
                articletext = soup.find_all('p')
                
        # combine text
        for paragraph in articletext:
            paragraphtext.append(paragraph.get_text())
            
        # combine all paragraphs into the body
        self.dictionary['body'] = "".join(paragraphtext)
        self.dictionary['body'] = " ".join(self.dictionary['body'].split()) #removes excessive whitespaces
        self.dictionary['body'] = self.dictionary['body'].strip("\n").strip(" ").strip("\t")
        self.dictionary['parsed'] = True
        
        print("Parsed article: " + self.dictionary['title'])

        # analyze the body for polarity and subjectivity
        if self.dictionary['parsed'] == True:
            textBlobObj = TextBlob(self.dictionary['body'])
            self.dictionary['sentiment'] = textBlobObj.sentiment
            self.dictionary['polarity'] = textBlobObj.sentiment.polarity
            self.dictionary['subjectivity'] = textBlobObj.sentiment.subjectivity
            self.dictionary['analyzed'] = True
    
    def __str__(self):
        return ("URL: " + self.dictionary['url'] +
            "\nParsed: " + str(self.dictionary['parsed']) +
            "\nAnalyzed: " + str(self.dictionary['analyzed']) +
            "\nSentiment: " + str(self.dictionary['sentiment']) +
            "\nPolarity: " + str(self.dictionary['polarity']) +
            "\nSubjectivity: " + str(self.dictionary['subjectivity']) +
            "\nTitle: " + self.dictionary['title'] +
            "\nAuthor: " + self.dictionary['author'] +
            "\nBody: " + self.dictionary['body'])
    
    def output(self, fn):
        if (self.dictionary['parsed']):
            if (file_is_empty(fn)): # if the file is empty, we must add our csv header
                f = open(fn, "w")
                print("URL,Parsed,Analyzed,Sentiment,Polarity,Subjectivity,Title,Author,Body", file=f)
                f.close()
            
            writeFile = open(fn, 'a')
            csv.writer(writeFile,  lineterminator='\n').writerow([
            	self.dictionary['url'], 
            	str(self.dictionary['parsed']), 
            	str(self.dictionary['analyzed']), 
            	str(self.dictionary['sentiment']), 
            	str(self.dictionary['polarity']), 
            	str(self.dictionary['subjectivity']), 
            	self.dictionary['title'], 
            	self.dictionary['author'], 
            	self.dictionary['body']])
                    
            writeFile.close()
            print("Article saved to csv file: " + self.dictionary['title'])
            
            
    
    def logerror(self, error):
        f = open(err_file, "a")
        print("URL: " + self.dictionary['url'], file=f)
        print("Error: " + error, file=f)
        print("", file=f)
        f.close()
        print(error + " logged in error file.")
        


def file_is_empty(path):
    try:
        f = open(path, "r")
        f.close()
        return False
    except:
        return True
