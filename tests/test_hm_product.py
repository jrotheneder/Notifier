import os,sys,json,requests

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.hm_product import HmProduct

url1 = 'https://www2.hm.com/de_at/productpage.1209975002.html'
url2 = 'https://www2.hm.com/de_at/productpage.1207938001.html'
url3 = 'https://www2.hm.com/de_at/productpage.0764938034.html'
url4 = 'https://www2.hm.com/de_at/productpage.1248149002.html'

url = url4

cp = HmProduct.fromUrlSize(url, "M") 

print(cp,"\n") 
cp.dict['price'] = 'over 9000'  

print(cp,"\n") 
print(cp.update())

