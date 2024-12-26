from .product import Product
from .hm_scraper import HmScraper
from .exceptions import *

class HmProduct(Product):
        
    def __init__(self, productDict):
        super().__init__(productDict)
        
    @classmethod
    def fromUrlSize(cls, url, size):
        
        return cls(HmScraper.getProductFromUrlSize(url, size))   
        
    def update(self):

        url = self.dict['url']
        size = self.dict['size']
        
        newDict = HmScraper.getProductFromUrlSize(url, size)    
                
        old_values = {}
        for key in self.dict.keys(): 
            if(self.dict[key] != newDict[key]):
                old_values[key] = self.dict[key]
        
        self.dict = newDict
            
        return [len(old_values), old_values]

    def productType(self):
        return "hm"

