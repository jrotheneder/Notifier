import os,sys,json,requests

# Add the src directory for the scraper module to allow importing 
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.uniqlo_scraper import *

url1 = 'https://www.uniqlo.com/eu-at/en/products/E463950-000/00?colorDisplayCode=06&sizeDisplayCode=004'
url2 = 'https://www.uniqlo.com/eu-at/en/products/E450543-000/01?colorDisplayCode=26&sizeDisplayCode=004'

url = url1

jsonObj = UniqloScraper.scrapeProductData(url)
# print(jsonObj)
print(json.dumps(jsonObj, indent=4, sort_keys=True))

print(UniqloScraper.getProductJson(url))
