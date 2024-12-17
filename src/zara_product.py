import sys,os

from product import Product
from zara_scraper import ZaraScraper

from exceptions import *

class ZaraProduct(Product):
        
    def __init__(self, productDict):
        super().__init__(productDict)
        
    @classmethod
    def fromUrlSku(cls, url, sku):

        productData = ZaraScraper.getProductFromSku(url, sku)
        return cls(productData)  
    
    @classmethod
    def fromUrlSize(cls, url, size):
        
        productData = ZaraScraper.getProductFromSize(url, size)
        return cls(productData)  

    def update(self):

        url = self.dict['url']
        sku = self.dict['sku']
        
        jsonObj = ZaraScraper.getProductList(url) 

        try: 
            new_product_dict = ZaraScraper.extract(jsonObj, url, sku)

        except SkuNotFoundException as ex:
           # in this case we don't raise again, but rather just mark the item as offline 
            new_product_dict = self.dict.copy()
            new_product_dict['status'] = 'offline (possibly, sku changed?)'  

        changed_values = {}
        for key in self.dict.keys(): 
            if(self.dict[key] != new_product_dict[key]):
                changed_values[key] = self.dict[key]
        
        self.dict = new_product_dict
        
        return [len(changed_values), changed_values]

    def updateSku(self):

        jsonObj = ZaraScraper.getProductList(self.dict['url'])

        # TODO this procedure generates 2 technically superflous accesses of the product
        # webpage, improve this 

        raise SkuNotFoundException("updating sku of product " + str(self) +
                              " failed in updateSku()")
    
    def productType(self):
        return "zara"
