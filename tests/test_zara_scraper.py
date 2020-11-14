import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zara_scraper import ZaraScraper
import requests

url2 = "https://www.zara.com/at/en/textured-sweater-p03332309.html"
url3 = "https://www.zara.com/at/en/leather-brogue-boots-p12020620.html"

print(json.dumps(ZaraScraper.getProductList(url2), indent=4,
    sort_keys=True))
print(json.dumps(ZaraScraper.getProductFromSize(url3, '43'), indent=4, sort_keys=True))
