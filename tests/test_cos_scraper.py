import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from cos_scraper import CosScraper
import requests

url1 = 'https://www.cosstores.com/en_eur/men/menswear/knitwear/jumpers/product.brushed-wool-crewneck-jumper-blue.0927488003.html'
url2 = 'https://www.cosstores.com/en_eur/men/menswear/suits/trousers/product.linen-tapered-leg-trousers-grey.0850709001.html'
url3 = 'https://www.cosstores.com/en_eur/productpage.0779141004.html'

data = CosScraper.getProductList(url3)
print(CosScraper.getProductFromUrl(url3)) 

#print(CosScraper.getProductFromSize(url2, 'M'))
