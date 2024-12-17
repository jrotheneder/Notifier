import requests
import bs4
import json
import re

from exceptions import SkuNotFoundException

class UniqloScraper:
    
    @staticmethod
    def getProductList(url):
        """ Obtain a json containing data on product variants corresponding
            to the given url (mostly size variations on Uniqlo) """
    
        # with html queries attached, the sku received varies (?)
        url = UniqloScraper.cleanUrl(url)
    
        headers = {'User-Agent': ("Mozilla/5.0 (Mcintosh; Intel Mac OS X 10_11_2)" 
                "AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9")}

        res = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(res.content,'html.parser')

        script = soup.find('script', text = re.compile('pdpVariationsJSON'))

        if(script == None):
            raise SkuNotFoundException("sku not found in getProductList(). Does the url " + url + " still exist?")

        jsonStr = script.contents[0]
        jsonStr = jsonStr[jsonStr.find('{') - 1 : jsonStr.rfind('}')+1]

        jsonObj = json.loads(jsonStr.replace("\n",""))

        if(jsonObj == None):
            raise SkuNotFoundException("sku not found in getProductList(). Does the url " + url + " still exist?")

            
        return jsonObj
    
    @staticmethod
    def cleanUrl(url):
        # with html queries attached, the sku received varies (?)
        return url.split('?')[0]

    @staticmethod
    def urlToColor(url):

        idx = url.find('COL') 

        if(idx == -1):
            raise SkuNotFoundException("couldn't determine color from url in \
                urlToColor() for uniqlo product" + url) 
        return  url[idx:idx+5] 

    @staticmethod
    def getProductFromSize(url, size):
        """ Given a json containing information on all variants of the item
        with a supplied url, returns a flattened and simplified json containing
        only essential info about the variant with a specified size"""
        
        unit = None

        color = UniqloScraper.urlToColor(url) 
        jsonObj = UniqloScraper.getProductList(url)

        for key, val in jsonObj.items():
            if(color in key and val['attributes']['size'] == size):
                unit = val

        if(unit == None):
            raise(SkuNotFoundException("size not found in extract()"))

        price = str(unit['pricing']['sale'])  
        sku = unit['id']
        stock = unit['availability']['ats']  
        in_stock_bool = 'InStock' if unit['availability']['inStock'] else 'OutOfStock'
        color = unit['attributes']['color']    

        productJson = {'sku':sku, 'url':url, 'price':price, 
                'size': size, 'stock' : stock, 'availability':
                in_stock_bool, 'color': color }
        
        return productJson
    
