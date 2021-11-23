import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zara_scraper import *
import requests

url2 = "https://www.zara.com/at/en/striped-shirt-p05571300.html?v1=123839133&v2=1886403"
url3 = "https://www.zara.com/at/en/leather-brogue-boots-p12020620.html"
url4 = "https://www.zara.com/at/en/black-chelsea-boots-p12000720.html"

url = url2

lst = ZaraScraper.getProductList(url)
print(ZaraScraper.skuSummary(lst))
print(ZaraScraper.getProductFromSku(url, "110483145"))
#print(ZaraScraper.getProductFromSize(url, "M"))
#print(json.dumps(ZaraScraper.getProductList(url), indent=4,
#    sort_keys=True))
