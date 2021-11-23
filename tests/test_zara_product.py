import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zara_product import ZaraProduct

def test(): 

    url2 = "https://www.zara.com/at/en/striped-shirt-p05571300.html?v1=123839133&v2=1886403"
    url3 = "https://www.zara.com/at/en/share/viscose-and-linen-shirt---limited-edition-p04177015.html"
    url4 = "https://www.zara.com/at/en/black-chelsea-boots-p12000720.html"

    zp = ZaraProduct.fromUrlSku(url2, "123839133-622-2")
    print(zp,"\n")

#   zp = ZaraProduct.fromUrlSize(url4, "43")
#   print(zp, "\n")

    zp.dict["price"] = "over 9000"  
    print(zp) 
    print(zp.update())

if __name__ == "__main__":

    test()
