import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from uniqlo_scraper import UniqloScraper
import requests

url1 = 'https://www.uniqlo.com/eu/en_AT/product/men-premium-lambswool-v-neck-cardigan-429069COL08SMA002000.html'
url2 = 'https://www.uniqlo.com/eu/en_AT/product/men-100pct-extra-fine-merino-wool-turtleneck-jumper-429067COL37SMA002000.html'
url3 = 'https://www.uniqlo.com/eu/en_AT/product/men-comfort-blazer-jacket-425422COL08SMA002000.html'
url4 = 'https://www.uniqlo.com/eu/en_AT/product/men-colour-socks-423540COL67MSC027000.html'

print(json.dumps(UniqloScraper.getProductList(url3), indent=4,
    sort_keys=True))

print(UniqloScraper.getProductFromSize(url2, 'M'))
