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
    tagRaw = ele.find_element(By.TAG_NAME, "span").text
    
    tagRaw = tagRaw.replace('및', '•').replace(' ','')
    
    tagList = tagRaw.split('•')
    
    del tagList[0]
    
    #print(tagList)
    return tagList
    
    
    
    
def get_image(driver):
    imgList = []
    
    wait = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='ItemsSlider-module__arrowButton___ZH7Ek commonStyles-module__basicButton___go-bX Button-module__iconButtonBase___uzoKc Button-module__basicBorderRadius___TaX9J Button-module__sizeIconButtonMedium___WJrxo Button-module__buttonBase___olICK Button-module__textNoUnderline___kHdUB Button-module__typeBrand___MMuct Button-module__overlayModeSolid___v6EcO']")))
    
    gallery = driver.find_elements(By.CSS_SELECTOR, "ol[class='ItemsSlider-module__wrapper___nAi6y']")
    
    
    imgClick = gallery[0].click()
    time.sleep(0.5)
    
    imgNumber = driver.find_element(By.CSS_SELECTOR, "h2[class='typography-module__xdsSubTitle1___N02-X']").text
    
    imgNumber = imgNumber[13:]
    imgNumber = int(imgNumber[:-1])
    
    
    
    
    for _ in range(0, imgNumber):
        img = driver.find_element(By.CSS_SELECTOR, "img[class='MediaItem-module__image___VlVzn']").get_attribute('src')
        imgList.append(img)
        time.sleep(1)
        nextBtn = driver.find_element(By.CSS_SELECTOR, "button[class='glyph-prepend glyph-prepend-chevron-right MediaViewerSlider-module__arrowButton___pc-7m Button-module__basicBorderRadius___TaX9J Button-module__defaultBase___c7wIT Button-module__buttonBase___olICK Button-module__textNoUnderline___kHdUB Button-module__typeTertiary___wNh6R Button-module__sizeMedium___T+8s+ Button-module__overlayModeSolid___v6EcO']")
        nextBtn.click()
    
    #print(imgNumber)
    #print(imgList)
    return imgList



def detail_scrap(driver, driver_eng, url, url_eng):
    
    autokwdSet = set()
    
    driver.implicitly_wait(10)
    driver_eng.implicitly_wait(10)
    
    
    driver.get(url)
    driver_eng.get(url_eng)
    
    title = driver.find_element(By.CSS_SELECTOR, "h1[data-testid='ProductDetailsHeaderProductTitle']").text
    engTitle = driver.find_element(By.CSS_SELECTOR, "h1[data-testid='ProductDetailsHeaderProductTitle']").text
    
    autokwdSet.add(title)
    autokwdSet.add(engTitle)
    
    autokwd = list(autokwdSet)
    
    
    thum = driver.find_element(By.CSS_SELECTOR, "img[class='ProductDetailsHeader-module__backgroundImage___34Nro img-fluid']").get_attribute('src')
    description = driver.find_element(By.CSS_SELECTOR, "p[class='Description-module__description___ylcn4 typography-module__xdsBody2___RNdGY ExpandableText-module__container___Uc17O']").text
    company = driver.find_element(By.CSS_SELECTOR, "div[class='typography-module__xdsBody2___RNdGY']").text
    tagList = get_tag(driver)
    screenList = get_image(driver)
    
    
    detail_dict = {
        'imageurl': thum,
        'description': description,
        'autokwd': autokwd,
        'company': company,
        'screenshot': screenList,
        'tag':tagList,
        'platform': ["xbox"]
    }
    
    print(detail_dict)
    
    return detail_dict