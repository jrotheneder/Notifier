import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from cos_product import CosProduct
import requests

url1 = 'https://www.cosstores.com/en_eur/men/menswear/knitwear/jumpers/product.brushed-wool-crewneck-jumper-blue.0927488003.html'
url2 = 'https://www.cosstores.com/en_eur/men/menswear/suits/trousers/product.linen-tapered-leg-trousers-grey.0850709001.html'
url3 = 'https://www.cosstores.com/en_eur/men/menswear/suits/blazers/product.cashmere-wool-mix-collarless-blazer-grey.0925206002.html'

cp = CosProduct.fromUrl(url3) 

print(cp,"\n") 
cp.dict['price'] = 'over 9000'  

print(cp,"\n") 
print(cp.update())

