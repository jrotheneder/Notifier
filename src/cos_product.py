from .product import Product
from .cos_scraper import CosScraper
from .exceptions import *

class CosProduct(Product):
        
    def __init__(self, productDict):
        super().__init__(productDict)
        
    @classmethod
    def fromUrl(cls, url):
        
        return cls(CosScraper.getProductFromUrl(url))   
        
    def update(self):

        url = self.dict['url']
        
        newDict = CosScraper.getProductFromUrl(url)    
                
#       if(len(self.dict) != len(newDict)):
#           raise RuntimeError("Error in update(): new dict has more items than old dict")
        
        old_values = {}
        for key in self.dict.keys(): 
            if(self.dict[key] != newDict[key]):
                old_values[key] = self.dict[key]
        
        self.dict = newDict
            
        return [len(old_values), old_values]

    def productType(self):
        return "cos"

