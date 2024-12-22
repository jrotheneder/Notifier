import requests
import bs4
import json
import re

from .exceptions import *

class ZaraScraper:
    
    numToSize = {'1':'XS', '2': 'S', '3': 'M', '4': 'L', '5': 'XL', '6': 'XXL'}
#           '32':'32', '34':'34', '36':'36', '38':'38', '40':'40', '42':'42',
#           '44':'44', '46':'46', '48':'48', '50':'50', '52':'52', '54':'54'}
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
        soup = bs4.BeautifulSoup(res.content, "html.parser")

        # NOTE: currently, this fix is not needed
        # The first requests.get does not give the required info, but we can
        # obtain it like here: https://stackoverflow.com/questions/77023797
#         url2 = "https://www.zara.com" + (
#             soup.select_one('meta[http-equiv="refresh"]')["content"]
#             .split("=", maxsplit=1)[-1]
#             .strip("'")
#         )
#         soup = bs4.BeautifulSoup(requests.get(url2, headers=headers).content,\
#                                  "html.parser")

        soup_result = soup.find_all("script", {"type" : "application/ld+json"})
        
        try: 
            assert(len(soup_result) == 1)
            json_str = soup_result[0].get_text()
            jsonObj = json.loads(json_str) 
#             print(json.dumps(jsonObj, indent=4)) 

        except:
            raise SkuNotFoundException("Nothing found in getProductList(). Does \
                    the url " + url + " still exist?")
            
        return jsonObj

    @staticmethod
    def skuSummary(jsonObj):
        """
        Given a jsonObj containing a list of products extracted from a zara url, 
        return a summary of the product variants available 
        """
        
        name = jsonObj[0]["name"]  

        # skus are of the form ProdString-ColString-SizeString, where
        # ProductString is shared among all instances of the same product,
        # colors are differentiated by ColString and sizes by SizeString. 
        # We now figure out how many different colors there are, and in which
        # sizes these colors are avilable. Note that SizeString is an int, which
        # we map to standard size strings using the numToSize (which is a guess
        # and not guaranteed to be right always). Usually, all colors have the
        # same sizes available.
        skus = [item["sku"] for item in jsonObj]  
        skus_sans_sizes = set(['-'.join(item.split('-')[:-1]) for item in skus]) 

        sizes = [item["size"] for item in jsonObj] # repeats elements 
        size_dict = { sku : size for sku, size in zip(skus, sizes) }

        # collect images and colors: 
        color_dict = {}
        image_url_dict = {}

        for item in jsonObj: 
            sku_sans_size = '-'.join(item["sku"].split('-')[:-1])

            image_url_dict[sku_sans_size] = item["image"]  
            color_dict[sku_sans_size] = item["color"]  


#       import pprint 
#       pp = pprint.PrettyPrinter(depth=4) 
#       pp.pprint(image_url_dict) 

        return [name, skus, skus_sans_sizes, size_dict, image_url_dict, color_dict]  

    @staticmethod
    def extract(jsonObj, url, sku): 
        """
        Given jsonObj and sku, extract relevant information about the item with
        the given sku
        """
        name = jsonObj[0]['name']

        for item in jsonObj: 
            if item["sku"] == sku:  # located item 
                
                # NOTE: as of late, sizes are explicitly given in the json
#                 size_name = sku.split('-')[-1]
#                 # convert 1,...6, to XS,...XL
#                 if size_name in ZaraScraper.numToSize: 
#                     size_name = ZaraScraper.numToSize[size_name]
                
                size_name = item["size"]
                offer = item["offers"]  
                price = offer["price"] + " " + offer["priceCurrency"]    
                color = item["color"]

                if "availability" in offer: # this suggests the item is available
                    availability = offer["availability"].split('/')[-1]     
                else: 
                    availability = "OutOfStock/Unknown"
                
                return {'sku' : sku, 'name' : name, 'url' : url, \
                        'price' : price, 'size' : size_name, 'status' : 'online', \
                        'availability' : availability, 'color' : color}  

        raise SkuNotFoundException("sku " + sku + ", " + url \
            + " not found in extract() (but > 0 skus found). "\
            + "Correct sku, item available?")
        
    @staticmethod
    def cleanUrl(url):
        # with html queries attached, the skus received vary, so we 
        # remove these queries to get consistency
        return url.split('?')[0]
               
    @staticmethod
    def getProductFromSku(url, sku):

        jsonObj = ZaraScraper.getProductList(url)
        return ZaraScraper.extract(jsonObj, url, sku) 

    @staticmethod
    def getProductFromSize(url, size):

        jsonObj = ZaraScraper.getProductList(url)

        # get summary of skus to check if there is only one item variant
        [name, skus, skus_sans_sizes, sizes, image_url_dict, color_dict] = \
                ZaraScraper.skuSummary(jsonObj)
        
        if(len(skus_sans_sizes) > 1):
            raise(RuntimeError("There seems to be more than one variant of this \
                product. Please provide the sku (query with the info command) instead \
                of the size."))
            
        # if the size is of the form XS, S, M, ... assume this corresponds to 
        # last digits 1,2,3,... in the sku. Otherwise, assume last two digits of
        # sku correspond exactly to size

        # NOTE: as of late, sizes are explicitly given in the json, so this 
        # brittle method is not needed at the moment
#         if size in ZaraScraper.sizeToNum: 
#             size = ZaraScraper.sizeToNum[size]

#         for sku in skus: 
#             if sku.split("-")[-1] == size: 
#                 return ZaraScraper.extract(jsonObj, url, sku)

        for item in jsonObj: 
            if item["size"] == size: 
                return ZaraScraper.extract(jsonObj, url, item["sku"])

        raise(RuntimeError("Size not found."))
