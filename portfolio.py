from company import Company
from utility import companies_from_csv

class Portfolio:
    def __init__(self, company_file = "companies.csv", url_fn = "urls.txt", id_ = 'p0001'):
        self.url_filename = url_fn # the filename where previously viewed urls are stored
        self.company_file = company_file
        self.id = id_
        
        self.companies = companies_from_csv(company_file)