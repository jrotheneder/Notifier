import requests, bs4, json, re, os, time, shutil
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .product import Product
from .webdriverhelper import WebDriverHelper
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
    def getProductList2(url):
        """ Obtain a json containing a list of products corresponding
            to the given url. This method differs from getProductList 
            in that it uses selenium, which is sometimes more accurate"""
    
        # with html queries attached, the sku received varies (?)
        url = ZaraScraper.cleanUrl(url)
    
        driver_helper = WebDriverHelper()
        driver = driver_helper.driver

        try:
            # Open a web page
            driver.get(url)

            # Wait for the <script type="application/ld+json"> element to load
            # the first time the json is loaded, it sometimes contains wrong 
            # data. We wait for a fixed amount of time, hoping that after that, 
            # the correct data is loaded. 
            # NOTE: if the availability of Uniqlo items is frequently wrong, 
            # increasing the wait time here might help.
            time.sleep(3) 
            page_source = driver.page_source
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, 
                    "//script[@type='application/ld+json']"))
            )

            # Get the fully loaded HTML

            # Parse the HTML, locate the script element and extract the json
            soup = bs4.BeautifulSoup(page_source, "html.parser")
            soup_result = soup.find_all("script", {"type" : "application/ld+json"})
            
            assert(len(soup_result) == 1)
            json_str = soup_result[0].get_text()
            jsonObj = json.loads(json_str) 

            return jsonObj 
            

        except Exception as ex:
            raise SkuNotFoundException(f"Exception {ex} occured in getProductList(). \n" \
                    f"Does the url {url} still exist?")
        finally:
            driver_helper.close()


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

        return [name, skus, skus_sans_sizes, size_dict, image_url_dict, color_dict]  

    @staticmethod
    def extract_helper(url, item):
        """
        Given a dict containing information about a single item, extract
        relevant information for further processing
        """

        # NOTE: as of late, sizes are explicitly given in the json
#       size_name = sku.split('-')[-1]
#       # convert 1,...6, to XS,...XL
#       if size_name in ZaraScraper.numToSize: 
#           size_name = ZaraScraper.numToSize[size_name]
        
        name = item["name"]
        size_name = item["size"]
        offer = item["offers"]  
        price = offer["price"] + " " + offer["priceCurrency"]    
        color = item["color"]
        sku = item["sku"]

        if "availability" in offer: # this suggests the item is available
            availability = offer["availability"].split('/')[-1]     
        else: 
            availability = "OutOfStock/Unknown"
        
        return {'sku' : sku, 'name' : name, 'url' : url, \
                'price' : price, 'size' : size_name, 'status' : 'online', \
                'availability' : availability, 'color' : color}  

    @staticmethod
    def extract_by_sku(jsonObj, url, sku): 
        """
        Given jsonObj and sku, extract relevant information about the item with
        the given sku
        """
        name = jsonObj[0]['name']

        for item in jsonObj: 
            if item["sku"] == sku:  # located item 
                return ZaraScraper.extract_helper(url, item)    

        raise SkuNotFoundException("sku " + sku + ", " + url \
            + " not found in extract_by_sku(). Correct sku, item available?")

    @staticmethod
    def extract_by_size_color(jsonObj, url, size, color_prefix): 
        """
        Given jsonObj and size and color, extract relevant information about the
        item with the given size and color
        """

        # check if there is a unique item in jsonObj with the right 
        # size and color_prefix
        items = [item for item in jsonObj 
            if (item["color"].startswith(color_prefix) and item["size"] == str(size))]

        if len(items) == 0: 
            raise ItemNotFoundException(f"No item found with size {size} and "
                f"color (prefix) {color_prefix}.")
        elif len(items) > 1: 
            raise ItemNotFoundException(f"Multiple items found with these \
                    properties. Is the color (prefix) {color_prefix} too short?")

        return ZaraScraper.extract_helper(url, items[0])
        
    @staticmethod
    def cleanUrl(url):
        """
        Removes all query parameters from a URL except for the 'v1' parameter, 
        which sometimes is the difference between an item being reachable 
        at the given url or not 
        """
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Keep only the 'v1' parameter
        filtered_params = {'v1': query_params.get('v1', [])}

        # Reconstruct the URL with the filtered parameters
        new_query = urlencode(filtered_params, doseq=True)
        new_parsed_url = parsed_url._replace(query=new_query)
        return urlunparse(new_parsed_url)
               
    @staticmethod
    def getProductFromSku(url, sku):

        jsonObj = ZaraScraper.getProductList(url)
        return ZaraScraper.extract_by_sku(jsonObj, url, sku) 

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
#                 return ZaraScraper.extract_by_sku(jsonObj, url, sku)

        for item in jsonObj: 
            if item["size"] == size: 
                return ZaraScraper.extract_by_sku(jsonObj, url, item["sku"])

        raise(SizeNotFoundException(f"Size {size} not found."))

    @staticmethod
    def getProductFromSizeColor(url, size, color_prefix):
        """
        Given a url, size and color_prefix, return a dict containing 
        essential information about the product with the given size and color
        """

        jsonObj = ZaraScraper.getProductList(url)
        return ZaraScraper.extract_by_size_color(jsonObj, url, size, color_prefix)
