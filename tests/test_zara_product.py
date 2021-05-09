import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zara_product import ZaraProduct

def test(): 

    url2 = "https://www.zara.com/at/en/comfort-flannel-trousers-p07380362.html?v1=84996070"
    url3 = "https://www.zara.com/at/en/share/viscose-and-linen-shirt---limited-edition-p04177015.html"

    zp = ZaraProduct.fromUrlSku(url2, "82273634")
    print(zp,"\n")

    zp = ZaraProduct.fromUrlSize(url3, "S")
    print(zp, "\n")

    zp.dict["price"] = "over 9000"  
    print(zp) 
    print(zp.update())

if __name__ == "__main__":

    test()
