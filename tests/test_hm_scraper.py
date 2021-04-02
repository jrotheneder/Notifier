import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from hm_scraper import HmScraper
import requests

url1 = 'https://www2.hm.com/de_at/productpage.0725358010.html'
url2 = 'https://www2.hm.com/de_at/productpage.0772570003.html'

url = url1

data = HmScraper.getProductList(url)
print(json.dumps(data, indent=4, sort_keys=True))

#print(HmScraper.getProductFromUrl(url)) 

