import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from cos_scraper import CosScraper
import requests

url1 = 'https://www.cosstores.com/en_eur/men/menswear/trousers/product.tapered-suit-trousers-black.0926118001.html'
url2 = 'https://www.cosstores.com/en_eur/men/menswear/trousers/product.tapered-suit-trousers-grey.0926118002.html'

url = url2

data = CosScraper.getProductList(url)
print(CosScraper.getProductFromUrl(url)) 

#print(CosScraper.getProductFromSize(url, 'M'))
