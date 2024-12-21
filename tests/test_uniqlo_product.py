import os,sys,json,requests
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from src.uniqlo_product import UniqloProduct

url1 = 'https://www.uniqlo.com/eu-at/en/products/E457622-000/00?colorDisplayCode=09&sizeDisplayCode=006'
url2 = 'https://www.uniqlo.com/eu-at/en/products/E450543-000/01?colorDisplayCode=26&sizeDisplayCode=004'

url = url2

up = UniqloProduct.fromUrl(url) 

print(up) 
up.dict['price'] = 'over 9000'  

print(up) 
print(up.update())
