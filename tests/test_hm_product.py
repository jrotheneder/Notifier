import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from hm_product import HmProduct
import requests

url1 = 'https://www2.hm.com/de_at/productpage.0772570002.html'
url2 = 'https://www2.hm.com/de_at/productpage.0772570003.html'

cp = HmProduct.fromUrl(url2) 

print(cp,"\n") 
cp.dict['price'] = 'over 9000'  

print(cp,"\n") 
print(cp.update())

