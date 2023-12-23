from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
#from core.logs.failedLog import failed_log
import time

# 태그 관련 함수 제작
# 고해상도의 이미지 링크를 얻기 위한 작업이 복잡해
# 별도의 get_image 함수로 분류

def get_tag(driver):
    ele = driver.find_element(By.CSS_SELECTOR, "div[class='typography-module__xdsSubTitle1___N02-X ProductDetailsHeader-module__productInfoLine___W-v+p']")
    tagRaw = ele.find_element(By.TAG_NAME, "span")
    
    tagRaw = tagRaw.replace('및', '•').replace(' ','')
    
    tagList = tagRaw.split('•')
    
    del tagList[0]
    
    print(tagList)
    return tagList
    
    
    
    
def get_image(driver):
    pass


def detail_scrap(driver, driver_eng):
    
    thum = driver.find_element(By.CSS_SELECTOR, "img[class='ProductDetailsHeader-module__backgroundImage___34Nro img-fluid']").get_attribute('src')
    description = driver.find_element(By.CSS_SELECTOR, "p[class='Description-module__description___ylcn4 typography-module__xdsBody2___RNdGY ExpandableText-module__container___Uc17O']").text
    company = driver.find_element(By.CSS_SELECTOR, "div[class='typography-module__xdsBody2___RNdGY']").text
    tag = get_tag(driver)