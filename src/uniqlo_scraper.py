import requests, bs4, json, re, os, time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .exceptions import *

class UniqloScraper:

    sizeCodes = {
        '001': 'XXS', 
        '002': 'XS',
        '003': 'S',
        '004': 'M',
        '005': 'L',
        '006': 'XL',
        '007': 'XXL',
        '008': '3XL',
        '009': '4XL'
    }

    colorCodes = {
        '06': 'Gray', 
        '07': 'Gray',
        '08': 'Dark Gray',
        '09': 'Black',
        '10': 'Pink',
        '26': 'Orange',
        '69': 'Navy'
    }

    @staticmethod
    def scrapeProductData(url):
        """ Obtain a json containing data on product variants corresponding
            to the given url (mostly size variations on Uniqlo) """

        # Path to WebDriver (assumed to be located in the parent dir of this file)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        webdriver_path = os.path.join(parent_dir, "chromedriver")
#         webdriver_path = "/home/ubuntu/Notifier/chromedriver"

        # Set up options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Enable headless (no gui) mode

        # Initialize WebDriver with headless mode
        service = Service(webdriver_path)
        driver = webdriver.Chrome(service=service, options=options)

        try:
            # Open a web page
            driver.get(url)

            # Wait for the <script type="application/ld+json"> element to load
            # the first time the json is loaded, it sometimes contains wrong 
            # data. We wait for a fixed amount of time, hoping that after that, 
            # the correct data is loaded. 
            # NOTE: if the availability of Uniqlo items is frequently wrong, 
            # increasing the wait time here might help.
            time.sleep(15) 
#             WebDriverWait(driver, 3).until(
#                 EC.presence_of_element_located((By.XPATH, 
#                     "//script[@type='application/ld+json']"))
#             )

            # Get the fully loaded HTML
            page_source = driver.page_source

            # Parse the HTML, locate the script element and extract the json
            soup = bs4.BeautifulSoup(page_source, 'html.parser')
            soup_result = soup.find_all("script", {"type" : "application/ld+json"})
            json_str = soup_result[0].get_text()
            jsonObj = json.loads(json_str) 

            return jsonObj 
            

        except Exception as ex:
            raise SkuNotFoundException(f"Exception {ex} occured in getProductList(). \n" \
                    f"Does the url {url} still exist?")
        finally:
            # Close and quit the browser
            driver.close()
            driver.quit()

            # on the server, chrome instances sometimes remain after calling driver.quit()
            os.system('killall chrome') 



    @staticmethod
    def urlToColorCode(url):
        """
        Extract the colorDisplayCode from the given URL.
        """
        pattern = r"colorDisplayCode=(\d+)"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            return None  # Return None if colorDisplayCode is not found

    @staticmethod
    def urlToSizeCode(url):
        """
        Extract the sizeDisplayCode from the given URL.
        """
        pattern = r"sizeDisplayCode=(\d+)"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            return None  # Return None if sizeDisplayCode is not found

    @staticmethod
    def getProductJson(url):
        """ Given a json containing information on the item at a supplied url,
        returns a flattened and simplified json containing essential info about
        the variant with a specified size"""
        
        jsonObj = UniqloScraper.scrapeProductData(url)
#         print(jsonObj)

        product_dict = jsonObj["@graph"][1]
        offer_dict = product_dict['offers']

        rating = product_dict['aggregateRating']['ratingValue']
        n_ratings = product_dict['aggregateRating']['reviewCount']

        price = str(offer_dict['price']) + ' ' + offer_dict['priceCurrency']

        availability = offer_dict['availability']
        colorCode = UniqloScraper.urlToColorCode(url) 
        sizeCode = UniqloScraper.urlToSizeCode(url)

        # as of late, uniqlo supplies no sku. We rely on skus to prevent 
        # duplicate additions, so we roll our own 
        mpn = product_dict['mpn']
        sku = mpn + "-" + colorCode + "-" + sizeCode

        # attempt translating (some) uniqlo color and size codes to 
        # a more readable format
        if sizeCode in UniqloScraper.sizeCodes.keys():
            sizeCode += " ("+ UniqloScraper.sizeCodes[sizeCode] + "?)"
        if colorCode in UniqloScraper.colorCodes.keys():
            colorCode += " ("+ UniqloScraper.colorCodes[colorCode] + "?)"

        productJson = {'sku':sku, 'url':url, 'price':price, 
                'size': sizeCode, 'availability': availability, 'colorCode': colorCode }
        
        return productJson
    
