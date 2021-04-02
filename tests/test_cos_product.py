import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from cos_product import CosProduct
import requests

url1 = 'https://www.cosstores.com/en_eur/men/menswear/trousers/product.tapered-suit-trousers-black.0926118001.html'
url2 = 'https://www.cosstores.com/en_eur/men/menswear/trousers/product.tapered-suit-trousers-grey.0926118002.html'

url = url1

cp = CosProduct.fromUrl(url) 

print(cp,"\n") 
cp.dict['price'] = 'over 9000'  

print(cp,"\n") 
print(cp.update())

