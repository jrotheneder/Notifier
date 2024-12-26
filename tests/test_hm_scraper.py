import os,sys,json,re
import requests

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.hm_scraper import HmScraper

url1 = 'https://www2.hm.com/de_at/productpage.1209975002.html'
url2 = 'https://www2.hm.com/de_at/productpage.1207938001.html'
url3 = 'https://www2.hm.com/de_at/productpage.0764938034.html'
url4 = 'https://www2.hm.com/de_at/productpage.1248149002.html'

url = url2

# data = HmScraper.getProductList(url)
data = HmScraper.scrapeProductData(url)
print(json.dumps(data, indent=4, sort_keys=True))

#print(HmScraper.getProductFromUrl(url)) 

