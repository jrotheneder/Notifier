import requests
import bs4
import json
import re

from exceptions import SkuNotFoundException
from jsoncomment import JsonComment # https://stackoverflow.com/questions/23705304/can-json-loads-ignore-trailing-commas

class CosScraper:
    
    @staticmethod
    def getProductList(url):
        """ Obtain a json containing data on product variants corresponding
            to the given url (mostly size variations on Cos) """
    
        # with html queries attached, the sku received varies (?)
        url = CosScraper.cleanUrl(url)
    
        headers = {'User-Agent': ("Mozilla/5.0 (Mcintosh; Intel Mac OS X 10_11_2)" 
                "AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9")}

        res = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(res.content,'html.parser')

        script = soup.find('script', text = re.compile('productArticleDetails'))

        if(script == None):
            raise SkuNotFoundException("sku not found in getProductList(). "
            " Does the url " + url + " still exist?")

        jsonStr = script.contents[0]
        jsonStr = jsonStr[jsonStr.find('{') - 1 : jsonStr.rfind('}')+1]
        jsonStr = jsonStr.replace('\'','\"').replace('\r','\n') 

        parser = JsonComment(json) 
        jsonObj = parser.loads(jsonStr) 

        if(jsonObj == None):
            raise SkuNotFoundException("sku not found in getProductList(). Does the url " + url + " still exist?")

        return jsonObj
    
    @staticmethod
    def cleanUrl(url):
        # with html queries attached, the sku received varies (?)
        return url.split('?')[0]

    @staticmethod
    def skuFromUrl(url): 

        pieces = url.split('.')
        index = pieces.index("html") - 1

        return pieces[index]  

    @staticmethod
    def getProductFromUrl(url):
        

        sku = CosScraper.skuFromUrl(url) 
        jsonObj = CosScraper.getProductList(url)

        unit = jsonObj[sku]  

        name = unit["title"]  
        price = unit["price"]  
        color = unit["colorLoc"]

        productJson = {'sku':sku, 'name' : name, 'url':url, 'price':price, 'color': color }
        
        return productJson
    
