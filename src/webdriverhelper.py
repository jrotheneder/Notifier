import requests, bs4, json, re, os, time, shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class WebDriverHelper:

    def __init__(self):
        # Path to WebDriver
        self.webdriver_path = shutil.which("chromedriver") #/usr/bin/chromedriver

        # Set up options
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")  # Enable headless (no gui) mode
#         self.options.add_argument('window-size=1200x800') # small window can help perf.
#         self.options.add_argument('--disable-extensions')  # Disable extensions
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        # Initialize WebDriver with headless mode
        self.service = Service(self.webdriver_path)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)


    def close(self):
        # Close and quit the browser
        if self.driver:
            self.driver.close()
            self.driver.quit()

        # on the server, chrome instances sometimes remain after calling driver.quit()
#             os.system('killall chrome') 
