from company import Company

class Portfolio:
    def __init__(self, company_file = "companies.txt", url_fn = "urls.txt"):
        self.url_filename = url_fn
        self.company_file = company_file
        
        
        # create companies dictionary from file
        self.companies = {}
        
        cp = open(company_file, "r")
        line = cp.readline()
        while (line):
            parts = line.split(">")
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
                self.companies.update({id_ : Company(name, stock, terms, blocked)})
            line = cp.readline()
        cp.close()