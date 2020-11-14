from product import Product
from uniqlo_scraper import UniqloScraper
from exceptions import *

class UniqloProduct(Product):
        
    def __init__(self, productDict):
        super().__init__(productDict)
        
    @classmethod
    def fromUrlSize(cls, url, size):
        
        return cls(UniqloScraper.getProductFromSize(url, size))   
        
    def update(self):

        url = self.dict['url']
        size = self.dict['size']
        
        newDict = UniqloScraper.getProductFromSize(url, size)    
                
#       if(len(self.dict) != len(newDict)):
#           raise RuntimeError("Error in update(): new dict has more items than old dict")
        
        old_values = {}
        for key in self.dict.keys(): 
            
            if(self.dict[key] != newDict[key]):

                # don't notify of a change if stock is still high
                if(key == 'stock' and int(newDict[key]) > Product.stock_msg_threshold):
                    continue 

                old_values[key] = self.dict[key]
        
        self.dict = newDict
            
        return [len(old_values), old_values]

    def updateSku(self):
        """
        Updating skus is not possible/sensible for uniqlo
        """
        
        raise SkuNotFoundException("updating sku of product " + str(self) +
                                  " failed in updateSku()")

    def productType(self):
        return "uniqlo"

