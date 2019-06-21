import requests
from bs4 import BeautifulSoup

err_file = "err.txt"

class Article:
  def __init__(self, url):
    self.url = url
    self.title = ""
    self.author = ""
    self.body = ""
    self.parsed = False
    self.analyzed = False
    

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
      print("Unparsed article logged in text file.")
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
    self.title = soup.title.get_text()

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
    return "URL: " + self.url + "\nParsed: " + str(self.parsed) + "\nTitle: " + self.title + "\nAuthor: " + self.author + "\nBody: " + self.body

  def output(self, fn):
    if (self.parsed):
      f = open(fn, "a")
      print(self, file=f)
      print("", file=f)
      f.close()
      print("Article saved to text file: " + self.title)
      
