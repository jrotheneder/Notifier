from product import Product
from zalando_scraper import ZalandoScraper
from exceptions import *

class ZalandoProduct(Product):
        
    def __init__(self, productDict):
        super().__init__(productDict)
        
    @classmethod
    def fromUrlSize(cls, url, size):
        
        return cls(ZalandoScraper.getProductFromSize(url, size))   
        
    def update(self):

        url = self.dict['url']
        size = self.dict['size']
        
        newDict = ZalandoScraper.getProductFromSize(url, size)    
                
        if(len(self.dict) != len(newDict)):
            raise RuntimeError("Error in update(): new dict has more items than old dict")
        
        old_values = {}
        for key in self.dict.keys(): 
            
            if(self.dict[key] != newDict[key]):

                # don't notify of a change if stock is still high
                if(key == 'stock' and int(newDict[key]) > Product.stock_msg_threshold): 
                    continue 

                old_values[key] = self.dict[key]
        
        self.dict = newDict
            
        return [len(old_values), old_values]

    def productType(self):
        return "zalando"
