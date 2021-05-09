import requests
import bs4
import json
import re

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

        p = re.compile(("zara\.viewPayload = ({.*});"))
        match = p.findall(str(soup))

        try: 

            assert(len(match) == 1)
            jsonStr2 = match[0]  
            jsonObj2 = json.loads(jsonStr2.replace("\n",""))

        except:
            raise SkuNotFoundException("sku not found in getProductList(). Does the url " + url + " still exist?")
            
        return jsonObj2["product"]  
    
    @staticmethod
    def getProductFromSku(url, sku):

        jsonObj = ZaraScraper.getProductList(url)
        return ZaraScraper.extract(jsonObj, url, sku) 

    @staticmethod
    def getProductFromSize(url, size):

        jsonObj = ZaraScraper.getProductList(url)
        [name, sku_sizes] = ZaraScraper.skuSummary(jsonObj)
        
        if(len(sku_sizes) > 1):
            raise(RuntimeError("There seems to be more than one variant of this \
                product. Need to construct with sku"))
            
        for color, skulist in sku_sizes.items():
            for sku_size in skulist:
                if(sku_size[1] == size): 

                    sku = sku_size[0]  
                    productData = ZaraScraper.extract(jsonObj, url, sku) 

                    return productData

    @staticmethod
    def extract(jsonObj, url, sku): 
        """
        Given jsonObj and sku, extract relevant information about the item with
        the given sku
        """
        product_name = jsonObj['name']

        for color in jsonObj["detail"]["colors"]:
            for size in color["sizes"]: 
                if(str(size["sku"]) == sku):  # found it 

                    price = str(size["price"])[0:2] + "." + str(size["price"])[2:4]   
                    size_name = size["name"]   
                    availability = size["availability"]  
                    color_name = color["name"]  
                    
                    return {'sku':sku, 'name':product_name, 'color':color_name, 'url':url,\
                        'price':price, 'size': size_name, 'availability':availability}  

        raise SkuNotFoundException("sku " + sku + " not found in extract() (but > 0 skus found). Correct sku?")

    @staticmethod
    def cleanUrl(url):
        # with html queries attached, the sku received varies (?)
        return url.split('?')[0]
               
    @staticmethod
    def skuSummary(jsonObj):
        
        name = jsonObj['name']
        sku_sizes = {}

        for color in jsonObj["detail"]["colors"]:
            sku_sizes[color["name"]] = [(str(size["sku"]), size["name"]) for size in color["sizes"]]  
        return [name, sku_sizes]
