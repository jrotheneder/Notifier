import os,sys,json,requests

# Add the src directory for the scraper module to allow importing 
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.zara_scraper import *
import test_zara_info


url1 = "https://www.zara.com/at/de/pullover-mit-geripptem-stehkragen-und-reissverschluss-p03284404.html?v1=410580976&v2=2432265"
url2 = "https://www.zara.com/at/de/abstrakter-jacquard-pullover-p09598397.html?v1=394906214&v2=2432265"
url3 = "https://www.zara.com/at/de/flanellhose-mit-zierfalten-p06861858.html?v1=412099077&v2=2432096"

url = url2
sku = "410580975-500-5"

jsonObj = ZaraScraper.getProductList(url)
# print(json.dumps(jsonObj, indent=4))
# print("\n\n")

[name, skus, skus_sans_sizes, sizes, image_url_dict, color_dict] \
        = ZaraScraper.skuSummary(jsonObj) 
print(ZaraScraper.skuSummary(jsonObj)) 
# print(skus)
# print(image_url_dict)
# print(color_dict)

# infoDict = ZaraScraper.extract(jsonObj, url, sku)  
# print(json.dumps(infoDict, indent=4))

# print(ZaraScraper.getProductFromSku(url, sku))
# print(ZaraScraper.getProductFromSize(url2, "L"))


print(test_zara_info.zara_item_info_helper(url1))
