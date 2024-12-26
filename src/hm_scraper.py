import requests, bs4, json, re, os, time, shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .product import Product
from .webdriverhelper import WebDriverHelper
from .exceptions import *

class HmScraper:

    @staticmethod
    def scrapeProductData(url):
        """ Obtain a json containing data on product variants corresponding
            to the given url (mostly size variations on Uniqlo) """

        driver_helper = WebDriverHelper()
        driver = driver_helper.driver

        try:
            # Open a web page
            driver.get(url)

            # Wait for the <script type="application/ld+json"> element to load
            # the first time the json is loaded, it sometimes contains wrong 
            # data. We wait for a fixed amount of time, hoping that after that, 
            # the correct data is loaded. 
            # NOTE: if the availability of items is frequently wrong, 
            # increasing the wait time here might help.
            time.sleep(2.5)
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, 
                    "//script[@type='application/ld+json']"))
            )

            # Get the fully loaded HTML
            page_source = driver.page_source

            # Parse the HTML, locate the script element and extract the json
            soup = bs4.BeautifulSoup(page_source, 'html.parser')

            soup_result_ldjson = soup.find_all("script", {"type" : "application/ld+json"})
            sou_result_appjson = soup.find_all("script", {"type" : "application/json"})

            json_str_ldjson = soup_result_ldjson[0].get_text()
            json_str_appjson = sou_result_appjson[0].get_text() 

            # Replace newlines in the "description" value which cause hiccups
            json_str_ldjson = re.sub(r'"description":\s*"([^"]*)"', 
                  lambda m: f'"description": "{m.group(1).replace("\n", " ")}"', 
                  json_str_ldjson)

            jsonObj_ldjson = json.loads(json_str_ldjson) 
            jsonObj_appjson = json.loads(json_str_appjson)

            # Get size data from appjson
            sku = jsonObj_ldjson["sku"]
            sizes = jsonObj_appjson["props"]["pageProps"]["productPageProps"]["aemData"]\
                   ["productArticleDetails"]["variations"][sku]["sizes"]

            jsonObj_ldjson["sizes"] = sizes

            return jsonObj_ldjson

        except Exception as ex:
            raise SkuNotFoundException(f"Exception {ex} occured in \
                    scrapeProductData().\nDoes the url {url} still exist?")

        finally:
            driver_helper.close()

    @staticmethod
    def cleanUrl(url):
        # with html queries attached, the sku received varies (?)
        return url.split('?')[0]

    @staticmethod
    def getProductFromUrlSize(url, size):
        
        jsonObj = HmScraper.scrapeProductData(url)

        short_sku = jsonObj["sku"]
        color = jsonObj["color"]
        name  = jsonObj["name"]
        size_data = jsonObj["sizes"] 
        available_sizes = [entry["name"] for entry in size_data]

        if size not in available_sizes:
            raise SkuNotFoundException(f"Size {size} not found for this \
                    product. Available sizes are {available_sizes}")
        else:
            # Find the correct sku for the item given the size
            long_sku = [entry["sizeCode"] for entry in size_data if entry["name"] ==
                        size][0] 

        offer = [entry for entry in jsonObj["offers"] if entry["SKU"] ==
                 long_sku][0]

        price = offer["price"]
        availability = offer["availability"].split('/')[-1]

        productJson = {'sku':long_sku, 'name' : name, 'url':url, 'price':price,
               'size': size, 'availability': availability, 'color': color }
        
        return productJson
    
