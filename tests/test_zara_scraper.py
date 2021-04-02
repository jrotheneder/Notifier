import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zara_scraper import *
import requests

url2 = "https://www.zara.com/at/en/comfort-flannel-trousers-p07380362.html?v1=84996070"
url3 = "https://www.zara.com/at/en/leather-brogue-boots-p12020620.html"

print(json.dumps(ZaraScraper.getProductList(url2), indent=4,
    sort_keys=True))
