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
        
        newDict = ZaraScraper.getProductFromSku(url, sku)    
                
        if(len(self.dict) != len(newDict)):
            raise RuntimeError("Error in update(): new dict has more items than old dict")
        
        changed_values = {}
        for key in self.dict.keys(): 
            
            if(self.dict[key] != newDict[key]):
                changed_values[key] = self.dict[key]
        
        self.dict = newDict
            
        return [len(changed_values), changed_values]
    
    def productType(self):
        return "zara"
