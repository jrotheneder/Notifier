from .product import Product
from .uniqlo_scraper import UniqloScraper
from .exceptions import *

class UniqloProduct(Product):
        
    def __init__(self, productDict):
        super().__init__(productDict)
        
    @classmethod
    def fromUrl(cls, url):
        
        return cls(UniqloScraper.getProductJson(url))   
        
    def update(self):

        url = self.dict['url']
        size = self.dict['size']

        try: 
            new_dict = UniqloScraper.getProductJson(url)    

        except SkuNotFoundException as ex:
           # in this case we don't raise again, but rather just mark the item as offline 
            new_dict = self.dict.copy()
            new_dict['status'] = 'offline/unreachable'  

        changed_values = {}
        for key in self.dict.keys(): 
            if(self.dict[key] != new_dict[key]):
                changed_values[key] = self.dict[key]
        
        self.dict = new_dict
        
        return [len(changed_values), changed_values]
        
    def productType(self):
        return "uniqlo"

