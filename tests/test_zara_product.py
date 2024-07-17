import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zara_product import ZaraProduct

def test(): 

    url2 = "https://www.zara.com/at/de/wide-fit-hose-mit-zierfalten-p00706260.html?v1=370119237&v2=2304180"
    url3 = "https://www.zara.com/at/de/anzugblazer-aus-reiner-wolle-limited-edition-p06364279.html?v1=294688263"
    url4 = "https://www.zara.com/at/de/pullover-mit-streifen-%E2%80%93-limited-edition-p00693325.html?v1=319992467"

    sku = "370119236-800-42"

    zp = ZaraProduct.fromUrlSku(url2, sku)
    print(zp,"\n")

#   zp = ZaraProduct.fromUrlSize(url4, "43")
#   print(zp, "\n")

    zp.dict["price"] = "over 9000"  
    print(zp) 
    print(zp.update())

if __name__ == "__main__":

    test()
