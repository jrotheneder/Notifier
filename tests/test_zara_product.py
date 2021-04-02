import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from zara_product import ZaraProduct

def test(): 

    url2 = "https://www.zara.com/at/en/comfort-flannel-trousers-p07380362.html?v1=84996070"
    url3 = "https://www.zara.com/at/en/leather-brogue-boots-p12020620.html"

    zp = ZaraProduct.fromUrlSku(url2, "83342030-800-3")
    print(zp,"\n")

    zp = ZaraProduct.fromUrlSize(url3, "46")
    print(zp, "\n")

    print(zp.update())

if __name__ == "__main__":

    test()
