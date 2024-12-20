from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

# Path to your WebDriver 
webdriver_path = "/home/johannes/ProgrammingProjects/Notifier/geckodriver"

# Set up Firefox options
options = Options()
options.add_argument("--headless")  # Enable headless mode

# Initialize WebDriver with headless mode
service = Service(webdriver_path)
driver = webdriver.Firefox(service=service, options=options)

try:
    # Open a web page
    driver.get("https://www.uniqlo.com/eu-at/en/products/E457622-000/00?colorDisplayCode=09&sizeDisplayCode=006")

    # Wait for JavaScript to load (can be replaced with WebDriverWait for specific elements)
    time.sleep(5)  # Replace with explicit waits for better performance

    # Get the fully loaded HTML
    page_source = driver.page_source
    print(page_source)

finally:
    # Close the browser
    driver.quit()

