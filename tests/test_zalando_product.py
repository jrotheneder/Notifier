import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zalando_product import ZalandoProduct

url1 = 'https://www.zalando.at/selected-homme-poloshirt-black-se622p03h-q11.html'
url2 = 'https://www.zalando.at/jack-jones-businesshemd-navy-blazer-ja222d0yq-k11.html'
url3 = 'https://www.zalando.at/puma-lqdcell-optic-xi-laufschuh-neutral-pu141a0gi-q11.html'

zp = ZalandoProduct.fromUrlSize(url3, "41")

print(zp) 

zp.dict['name']   = 'changed'
print(zp.update())

