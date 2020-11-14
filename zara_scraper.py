import requests
import bs4
import json
#import re

from exceptions import *

class ZaraScraper:
    
    numToSize = {'1':'XS', '2': 'S', '3': 'M', '4': 'L', '5': 'XL', '6': 'XXL'}
    sizeToNum = {'XS':'1', 'S':'2', 'M':'3', 'L':'4', 'XL':'5', 'XXL':'6'}

    @staticmethod
    def getProductList(url):
        """ Obtain a json containing a list of products corresponding
            to the given url"""
    
        # with html queries attached, the sku received varies (?)
        url = ZaraScraper.cleanUrl(url)
    
        headers = {'User-Agent': ("Mozilla/5.0 (Mcintosh; Intel Mac OS X 10_11_2)" 
                "AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9")}

        res = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(res.content,'html.parser')

        scripts = soup.find_all('script')
        jsonObj = None

        for script in scripts:
            if len(script.contents) and '@context' in script.contents[0]\
                and 'description' in script.contents[0]:

                jsonStr = script.contents[0]
                jsonObj = json.loads(jsonStr.replace("\n",""))

        if(jsonObj == None):
            raise SkuNotFoundException("sku not found in getProductList(). Does the url " + url + " still exist?")
            
        return jsonObj
    
    @staticmethod
    def getProductFromSku(url, sku):
        
        #logging.info("url = " + url + " sku = " + sku)

        jsonObj = ZaraScraper.getProductList(url)
        productJson = ZaraScraper.extract(jsonObj, sku)
        
        return ZaraScraper.compress(productJson)
    
    @staticmethod
    def cleanUrl(url):
        # with html queries attached, the sku received varies (?)
        return url.split('?')[0]
               
    @staticmethod
    def extract(jsonObj, sku):
        """ Given a list of skus and an individual sku, returns 
        a json containing the essential information about that sku
        """
        
        
        for product in jsonObj:
            if(product['sku'] == sku):
                return product

        raise(SkuNotFoundException("sku not found in extract()"))
    
    @staticmethod
    def compress(productJson):
        """ Given a json describing an individual sku, returns 
        a flattened and simplified json containing only essential info"""

        sku = productJson['sku']
        name = productJson['name']
        url = productJson['offers']['url']
        price = productJson['offers']['price']
        size = ZaraScraper.skuToSize(sku)
        availability = productJson['offers']['availability'].split("/")[-1]

        return {'sku':sku, 'name':name, 'url':url, 'price':price, 
                'size': size, 'availability':availability}  
    
    @staticmethod
    def skuSummary(url):
        
        jsonObj = ZaraScraper.getProductList(url)
        
        name = jsonObj[0]['name']

        # determine trimmed skus (with sizes trimmed, i.e. one 
        # per variant) as well as offered sizes
        skus = [product['sku'] for product in jsonObj]
        
        sizes = sorted(list(set([sku.split('-')[-1] for sku in skus])))
        skus = sorted(list(set(ZaraScraper.trimSku(sku) 
            for sku in skus)))
        
        rep_skus = [sku + "-" + sizes[0] for sku in skus]
        images = {ZaraScraper.trimSku(p['sku']) : p['image'][:-1] 
                  for p in jsonObj if p['sku'] in rep_skus}
        
        return [name, skus, sizes, images]
        
    
    @staticmethod
    def printProductList(url):
        """ Pretty print output of getProductList() """
        
        jsonObj = ZaraScraper.getProductList(url)

        for product in jsonObj:
            name = product['name']
            sku = product['sku']
            price = product['offers']['price']
            availabililty = product['offers']['availability'].split('/')[-1]

            print('Name: %s   SKU: %s   Price: %0.2f  Availability: %s' %(name,
                sku, float(price), availabililty))
            
    @staticmethod
    def trimSku(sku):
        return '-'.join(sku.split('-')[0:2])
    
    @staticmethod            
    def skuList(jsonObj):
        """return list of (trimmed) skus found in jsonObj (i.e. 
        one per item variant)
        """
        
        skus = [product['sku'] for product in jsonObj]
        skus = list(set(ZaraScraper.trimSku(sku) for sku in skus))
                
        return skus
    
    @staticmethod    
    def skuToSize(sku):
    
        sizeStr = sku.split('-')[-1]

        if(len(sizeStr) == 1):
            sizeStr = ZaraScraper.numToSize[sizeStr]
    
        return sizeStr
    
    @staticmethod
    def sizeToSkuPostfix(size):
        
        
        if(size.isnumeric()):
            return size
        else:
            try: 
                return ZaraScraper.sizeToNum[size]
            except KeyError:
                raise RuntimeError("Invalid Size")
