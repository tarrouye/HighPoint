import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

err_file = "err.txt"

class Article:
    def __init__(self, url = "", parsed = False, analyzed = "False", title = "", author = "", body = ""):
        self.url = url
        self.title = title
        self.author = author
        self.body = body
        self.parsed = parsed
        self.analyzed = analyzed

    def parse(self):
        paragraphtext = []
        # get page text and parse with BFS
        print("requesting page")
        # catch timeout errors and other request exceptions
        try:
            page = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
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
            
        self.author = aname
        
        # get article title or log error
        try:
            title = soup.title.get_text()
        except:
            title = ""
            self.logerror("Title Not Found")
            
        self.title = title
        
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
        self.body = "".join(paragraphtext)
        self.body = " ".join(self.body.split()) #removes excessive whitespaces
        self.parsed = True
        
        print("Parsed article: " + self.title)

        # analyze the body for polarity and subjectivity
        if self.parsed == True:
            textBlobObj = TextBlob(self.body)
            self.analyzed = textBlobObj.sentiment
    
    def __str__(self):
        return "URL: " + self.url + "\nParsed: " + str(self.parsed) + "\nAnalyzed: " + str(self.analyzed) + "\nTitle: " + self.title + "\nAuthor: " + self.author + "\nBody: " + self.body
        
    def output(self, fn):
        if (self.parsed):
            f = open(fn, "a")
            print(self, file=f)
            print("", file=f)
            f.close()
            print("Article saved to text file: " + self.title)
    
    def logerror(self, error):
        f = open(err_file, "a")
        print("URL: " + self.url, file=f)
        print("Error: " + error, file=f)
        print("", file=f)
        f.close()
        print(error + " logged in error file.")
        