from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

url1 = "https://example.com/"
url2 = "https://www.uniqlo.com/eu-at/en/products/E457622-000/00?colorDisplayCode=06&sizeDisplayCode=004"

url = url2

# Path to your WebDriver 
webdriver_path = "/home/ubuntu/Notifier/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)

# Initialize WebDriver with headless mode
service = Service(webdriver_path)

# Initialize ChromeDriver with service and options
driver = webdriver.Chrome(service=service, options=options)

try:
    print("Point 1\n", flush=True) 

    # Open a web page
    driver.get(url)

    print("Point 2\n", flush=True) 
    time.sleep(1)  # Replace with explicit waits for better performance

    # Get the fully loaded HTML
    page_source = driver.page_source
    print(page_source)
 

finally:
    # Close the browser
    driver.close()
    driver.quit()

