import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zara_scraper import *
import requests

url2 = "https://www.zara.com/at/de/pullover-aus-viskosemischgewebe-p00304300.html?v1=277277975&v2=2214634"
url3 = "https://www.zara.com/at/de/anzugblazer-aus-reiner-wolle-limited-edition-p06364279.html?v1=294688263"
url4 = "https://www.zara.com/at/de/pullover-mit-streifen-%E2%80%93-limited-edition-p00693325.html?v1=319992467"

url = url3

jsonObj = ZaraScraper.getProductList(url)
[name, skus, skus_sans_sizes, image_url_dict] = ZaraScraper.skuSummary(jsonObj) 
infoDict = ZaraScraper.extract(jsonObj, url, "309888211-801-50")  

print(ZaraScraper.getProductFromSku(url, "309888211-801-50"))
print(ZaraScraper.getProductFromSize(url4, "L"))
#print(json.dumps(ZaraScraper.getProductList(url), indent=4,
#    sort_keys=True))
