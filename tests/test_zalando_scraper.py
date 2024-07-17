import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zalando_scraper import ZalandoScraper
import requests

url1 = 'https://www.zalando.at/next-short-sleeve-regular-fit-poloshirt-brown-nx322q0uj-o11.html'

url = url1

print(json.dumps(ZalandoScraper.getProductList(url), indent=4,
    sort_keys=True))
print(json.dumps(ZalandoScraper.getProductFromSize(url, '30x32'), indent=4, sort_keys=True))
