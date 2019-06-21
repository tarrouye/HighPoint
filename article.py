import requests
from bs4 import BeautifulSoup

err_file = "err.txt"

class Article:
    def __init__(self, url = "", parsed = False, analyzed = False, title = "", author = "", body = ""):
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
        try:
            page = requests.get(self.url, timeout=30)
        except requests.exceptions.RequestException as e:
            print(e)
            f = open(err_file, "a")
            print("URL: " + self.url, file=f)
            print("Error: " + str(e), file=f)
            f.close()
            print("Unparsed article logged in error file.")
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
    
        # get article title
        try:
            title = soup.title.get_text()
        except:
            title = ""
            f = open(err_file, "a")
            print("URL: " + self.url, file=f)
            print("Error: Title Not Found", file=f)
            f.close()
            print("Title-less article logged in error file.")
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
    
    def __str__(self):
        return "URL: " + self.url + "\nParsed: " + str(self.parsed) + "\nAnalyzed: " + str(self.analyzed) + "\nTitle: " + self.title + "\nAuthor: " + self.author + "\nBody: " + self.body

    def output(self, fn):
        if (self.parsed):
            f = open(fn, "a")
            print(self, file=f)
            print("", file=f)
            f.close()
            print("Article saved to text file: " + self.title)
