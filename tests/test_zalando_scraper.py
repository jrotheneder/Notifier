import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zalando_scraper import ZalandoScraper
import requests

url1 = 'https://www.zalando.at/selected-homme-poloshirt-black-se622p03h-q11.html'
url2 = 'https://www.zalando.at/jack-jones-businesshemd-navy-blazer-ja222d0yq-k11.html'
url3 = 'https://www.zalando.at/puma-lqdcell-optic-xi-laufschuh-neutral-pu141a0gi-q11.html'
url4 = 'https://www.zalando.at/zign-unisex-set-tagesrucksack-black-zi154o01b-q11.html'

url = url4

print(json.dumps(ZalandoScraper.getProductList(url), indent=4,
    sort_keys=True))
print(json.dumps(ZalandoScraper.getProductFromSize(url, 'One Size'), indent=4, sort_keys=True))
