class Company:
  def __init__(self, name = "", stock = "", terms = [], blacklist = []):
    self.name = name
    self.search_terms = terms
    self.stock_symbol = stock
    self.blacklist = blacklist

    print("created__")
    print(name)
    print(stock)
    print(terms)
    print(blacklist)
    print("___")

  def block(self, url):
    self.blacklist.append(url)
