# import search api
import googlesearch
search = googlesearch.search
search_news = googlesearch.search_news

from article import Article
from company import Company

output_filename = 'out.txt'
url_filename = 'urls.txt'

# create companies dictionary from file
companies = {}

cp = open("companies.txt", "r")
line = cp.readline()
while (line):
	parts = line.split(">")
	for part in parts:
		part = part.strip(" ")
		part = part.strip("\n")
	if len(parts) > 1:
		id_ = parts[0].strip(" ")
		name = parts[1].strip(" ")
		stock = parts[2].strip(" ")
		terms = []
		for term in parts[3].split(","):
			term = term.strip(" ")
			term = term.strip("\n")
			if (term != ""):
				terms.append(term)
		blocked = []
		for block in parts[4].split(","):
			block = block.strip(" ")
			block = block.strip("\n")
			if (block != ""):
				blocked.append(block)
		companies.update({id_ : Company(name, stock, terms, blocked)})

	line = cp.readline()
cp.close()

# create used_url list from file
#print("URLS already considered: ")
used_urls = []
try:
	up = open(url_filename, "r")
	line = up.readline()
	while (line):
		used_urls.append(line.strip("\n"))
		#print(line)
		line = up.readline()
	up.close()
	print()
except:
	print("no url file yet")

#create articles list
articles = []

# check out the company list and populate article list
for cID in companies:
	company = companies[cID]
	print(company.name + ":", end = " ")
	for term in company.search_terms:
		print(term, end = ", ")
	print()

	print("Search Results for " + company.name + ": ")
	for term in company.search_terms:
		for url in search_news(term, stop = 25):
			url = url.strip(" ")
			url = url.strip("\n")
			print(url)
			if not url in used_urls:
				f = open(url_filename, "a")
				print(url, file=f)
				f.close()
				used_urls.append(url)
				print("URL saved to text file")
				#check if url is blacklisted or should be considered
				allow = True
				for block in company.blacklist:
					if block in url:
						allow = False
						print("URL was removed from consideration due to blacklist entry: " + block)
						break
				if allow:
					this_article = Article(url)
					this_article.parse() #parse it
					this_article.output(output_filename) #output to files
					articles.append(this_article)
			else:
				print("URL has already been considered.")
			print()
	print()
