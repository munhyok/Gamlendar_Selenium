from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re

from selenium import webdriver


driver = webdriver.Chrome()
def get_description(driver):
    
    rawTextList = []
    description = None
    descRaw = driver.find_element(By.CLASS_NAME, 'product.attribute.mfr_description').find_element(By.CLASS_NAME, 'value').find_elements(By.TAG_NAME,'p')
    
    if descRaw != []:
        for rawText in descRaw:
            rawTextList.append(rawText.text)
            description = "\n".join(rawTextList)
            
            return description
        
    
    else:  
        description = driver.find_element(By.CLASS_NAME, 'product.attribute.mfr_description').find_element(By.CLASS_NAME, 'value').text 
        
        return description


driver.get('https://store.nintendo.co.kr/70010000074078')
get_description(driver)