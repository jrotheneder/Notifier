from product import Product
from hm_scraper import HmScraper
from exceptions import *

class HmProduct(Product):
        
    def __init__(self, productDict):
        super().__init__(productDict)
        
    @classmethod
    def fromUrl(cls, url):
        
        return cls(HmScraper.getProductFromUrl(url))   
        
    def update(self):

        url = self.dict['url']
        
        newDict = HmScraper.getProductFromUrl(url)    
                
#       if(len(self.dict) != len(newDict)):
#           raise RuntimeError("Error in update(): new dict has more items than old dict")
        
        old_values = {}
        for key in self.dict.keys(): 
            if(self.dict[key] != newDict[key]):
                old_values[key] = self.dict[key]
        
        self.dict = newDict
            
        return [len(old_values), old_values]

    def productType(self):
        return "hm"

