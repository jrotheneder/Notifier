import sys,os

from .product import Product
from .zara_scraper import ZaraScraper

from .exceptions import *

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

    @classmethod
    def fromUrlSizeColor(cls, url, size, color):
        
        productData = ZaraScraper.getProductFromSizeColor(url, size, color)
        return cls(productData)  

    def update(self):

        url = self.dict['url']
        sku = self.dict['sku']
        color = self.dict['color']
        
        jsonObj = ZaraScraper.getProductList(url) 

        try: 
            new_product_dict = ZaraScraper.extract_by_sku(jsonObj, url, sku)

        except SkuNotFoundException as ex:

            try: # skus can change, so we try to find the product by color and size
                new_product_dict = ZaraScraper.extract_by_size_color(jsonObj, url, 
                                        self.dict['size'], color)

            except ItemNotFoundException as ex:
            # if the item cannot be found, we don't raise again, 
            # but rather just mark it as offline 
                new_product_dict = self.dict.copy()
                new_product_dict['status'] = 'offline (possibly, sku changed?)'  

        old_values = {}
        for key in self.dict.keys(): 
            if(self.dict[key] != new_product_dict[key]):
                old_values[key] = self.dict[key]
        
        self.dict = new_product_dict
        
        return [len(old_values), old_values]


    def productType(self):
        return "zara"
