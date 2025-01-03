import re, requests, json, bs4
from pprint import pprint

from .exceptions import SkuNotFoundException

class ZalandoScraper:
    
    @staticmethod
    def getProductList(url):
        """ Obtain a json containing data on product variants corresponding
            to the given url (mostly size variations on Zalando) """
    
        # with html queries attached, the sku received varies (?)
        url = ZalandoScraper.cleanUrl(url)
    
        headers = {'User-Agent': ("Mozilla/5.0 (Mcintosh; Intel Mac OS X 10_11_2)" 
                "AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9")}

        res = requests.get(url, headers=headers)

        # print res.content to file for inspection: 
        with open('zalando.html', 'w') as f:
            f.write(res.text)

        # the info we need is curreently contained between the parentheses
        # of runtime['hydratePartial'](...);. ... ends with }} which we 
        # match as well for more specificity 
        match = re.search(r"runtime\['hydratePartial'\]\((.*?)}}\);", res.text)
        if match:
            json_str = match.group(1) + "}}"
            print(json_str)
#             json_obj = json.loads(json_str)
#             print(json.dumps(json_obj, indent=2))

        soup = bs4.BeautifulSoup(res.content,'html.parser')

        soup_result = soup.find_all("script", {"type" : "application/ld+json"})

        try: 
            assert(len(soup_result) == 1)
            json_str = soup_result[0].get_text()
            jsonObj = json.loads(json_str) 
#           print(json.dumps(jsonObj, indent=3)) 

        except:
            raise SkuNotFoundException("Nothing found in getProductList(). Does \
                    the url " + url + " still exist?")
            
        return jsonObj
    
    @staticmethod
    def cleanUrl(url):
        # with html queries attached, the sku received varies (?)
        return url.split('?')[0]

    @staticmethod
    def getProductFromSize(url, size):
        
        #logging.info("url = " + url + " size = " + size)

        jsonObj = ZalandoScraper.getProductList(url)
        productJson = ZalandoScraper.extract(jsonObj, size)

        productJson['url'] = url # this info is not available in the json
        
        return productJson
    
               
    @staticmethod
    def extract(jsonObj, size):
        """ Given a json containing information on all variants of the item
        with a supplied url, returns a flattened and simplified json containing
        only essential info about the variant with a specified size"""
        
        name = jsonObj['name']  
        unit = None

        if(len(size) > 2): # non integer sizes like 42 1/3 are input as 42_1/3
            size = size.replace('_',' ') 

        for u in jsonObj['units']  :
            if(u['size']['local']  == size):
                unit = u

        if(unit == None):
            raise(SkuNotFoundException("size not found in extract(). Note that \
                sizes like 42 1/3 need to be input as 42_1/3."))
    
        price = unit['price']['value']  
        sku = unit['id']
        stock = unit['stock']

        return {'sku':sku, 'name':name, 'price':price, 'size': size, 'stock' : stock}  
    
