import requests, bs4, json, re, os, time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


url1 = "https://example.com/"
url2 = "https://www.uniqlo.com/eu-at/en/products/E457622-000/00?colorDisplayCode=06&sizeDisplayCode=004"

url = url2

# Path to your WebDriver 
webdriver_path = "/home/ubuntu/Notifier/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)

# experiment with some options to make selenium faster
options.add_argument('window-size=1200x800')
options.add_argument('--disable-extensions')  # Disable extensions
options.add_argument('--no-sandbox')  # Disable sandboxing 

prefs = {
    "profile.managed_default_content_settings.images": 2,  # Disable images
    "profile.managed_default_content_settings.stylesheets": 2,  # Disable CSS
}
options.add_experimental_option("prefs", prefs)


# Initialize WebDriver with headless mode
service = Service(webdriver_path)

# Initialize ChromeDriver with service and options
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(120)  # Timeout for page loading

try:
    print("Point 1 (entered try) \n", flush=True) 

    # Open a web page
    driver.get(url)

    print("Point 2 (called driver.get(url))\n", flush=True) 
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, 
            "//script[@type='application/ld+json']"))
    )
    time.sleep(60)

    # Get the fully loaded HTML
    page_source = driver.page_source

    # Parse the HTML, locate the script element and extract the json
    soup = bs4.BeautifulSoup(page_source, 'html.parser')
    soup_result = soup.find_all("script", {"type" : "application/ld+json"})
    json_str = soup_result[0].get_text()
    jsonObj = json.loads(json_str) 

    product_dict = jsonObj["@graph"][1]
    availability = product_dict['offers']['availability']

    print(json.dumps(product_dict, indent=2))
    print(availability)

finally:
    # Close the browser
    driver.close()
    driver.quit()

