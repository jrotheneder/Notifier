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
        
        jsonObj = ZaraScraper.getProductList(url)
        skus = ZaraScraper.skuList(jsonObj)
        
        if(len(skus) > 1):
            raise(RuntimeError("There seems to be more than one variant of this \
                product. Need to construct with sku"))
            
        desiredSku = skus[0] + "-" + ZaraScraper.sizeToSkuPostfix(size)
        productData = ZaraScraper.compress(
            ZaraScraper.extract(jsonObj, desiredSku))
        
        return cls(productData)   
        
    def update(self):

        url = self.dict['url']
        sku = self.dict['sku']
        
        newDict = ZaraScraper.getProductFromSku(url, sku)    
                
        if(len(self.dict) != len(newDict)):
            raise RuntimeError("Error in update(): new dict has more items than old dict")
        
        old_values = {}
        for key in self.dict.keys(): 
            
            if(self.dict[key] != newDict[key]):
                old_values[key] = self.dict[key]
        
        self.dict = newDict
            
        return [len(old_values), old_values]
    
    def updateSku(self):
        
        jsonObj = ZaraScraper.getProductList(self.dict['url'])
        new_skus = ZaraScraper.skuList(jsonObj) #trimmed skus ie no size
        
        old_sku = self.dict['sku'] #untrimmed
        
        if(len(new_skus) == 1): # one variant
            
            size_postfix = old_sku.split("-")[-1]
            new_sku = new_skus[0] + "-" + size_postfix
            
            self.dict['sku'] = new_sku
            
            return self.update()

        
        elif(len(new_skus) > 1): # more than one variant
        
            for sku in new_skus:

                #check if three digit variant ID agrees (this assumes 
                # that said three digit ID does not change on ZARA's side)
                if(sku.split('-')[-1] == old_sku.split('-')[-2]):

                    new_sku = old_sku.split('-')
                    new_sku[0] = sku.split('-')[0]
                    self.dict['sku'] = '-'.join(new_sku)

                    return self.update()
                
            
        raise SkuNotFoundException("updating sku of product " + str(self) +
                                  " failed in updateSku()")
    
    def productType(self):
        return "zara"
