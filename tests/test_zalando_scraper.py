import os,sys,json,requests

# Add the src directory for the zara_scraper module to allow importing 
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.zalando_scraper import *


url1 = 'https://www.zalando.at/scotch-and-soda-new-cup-sneaker-low-white-sc312o04t-a11.html'
url2 = 'https://www.zalando.at/suri-frey-tagesrucksack-black-sue54o00f-q11.html'
url3 = 'https://www.zalando.at/reebok-classic-hexalite-legacy-15-unisex-sneaker-low-alabasterfootwear-whitechalk-re015o0kl-a12.html'
url4 = 'https://www.zalando.at/new-balance-u327c-unisex-sneaker-low-olivine-ne215o0an-m12.html'

url = url4

jsonObj = ZalandoScraper.getProductList(url)
print(json.dumps(jsonObj, indent=4, sort_keys=True))

# print(json.dumps(ZalandoScraper.getProductFromSize(url, '30x32'), indent=4, sort_keys=True))
