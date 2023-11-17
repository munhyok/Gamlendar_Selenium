
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import date
from datetime import datetime
import datetime

def doScrollDown(whileSeconds, driver):
    
    element = driver.find_element(By.TAG_NAME, 'html')
    
    for i in range(whileSeconds):
        element.send_keys(Keys.ARROW_DOWN)