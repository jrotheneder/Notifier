import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zara_product import ZaraProduct

def test(): 

    url2 = "https://www.zara.com/at/de/pullover-aus-viskosemischgewebe-p00304300.html?v1=277277975&v2=2214634"
    url3 = "https://www.zara.com/at/de/anzugblazer-aus-reiner-wolle-limited-edition-p06364279.html?v1=294688263"
    url4 = "https://www.zara.com/at/de/pullover-mit-streifen-%E2%80%93-limited-edition-p00693325.html?v1=319992467"

    zp = ZaraProduct.fromUrlSku(url3, "309888211-801-50")
    print(zp,"\n")

#   zp = ZaraProduct.fromUrlSize(url4, "43")
#   print(zp, "\n")

    zp.dict["price"] = "over 9000"  
    print(zp) 
    print(zp.update())

if __name__ == "__main__":

    test()
