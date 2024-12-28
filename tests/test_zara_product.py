import os,sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from src.zara_product import ZaraProduct

url2 = "https://www.zara.com/at/de/wide-fit-hose-mit-zierfalten-p00706260.html?v1=370119237&v2=2304180"
url3 = "https://www.zara.com/at/de/strick-poloshirt-aus-baumwolle-und-seide-p00077304.html?v1=364086737&v2=2432049"
url4 = "https://www.zara.com/at/de/t-shirt-aus-strick-mit-abstraktem-muster-p07140301.html?v1=364740786"

url = url3

sku = "364086737-401-4"
# zp = ZaraProduct.fromUrlSize(url, "M")
# zp = ZaraProduct.fromUrlSizeColor(url, 38, "Beige")
zp = ZaraProduct.fromUrlSku(url, sku)
print(zp,"\n")

#   zp = ZaraProduct.fromUrlSize(url4, "43")
#   print(zp, "\n")

zp.dict["price"] = "over 9000"  
zp.dict["sku"] = "364086740-401-3"
zp.dict["url"] = "https://www.zara.com/at/de/strick-poloshirt-aus-baumwolle-und-seide-p00077304.html?v1=364086737&v2=2432049"

print(zp,"\n") 
print(zp.update(), "\n")
print(zp,"\n") 

