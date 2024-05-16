from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
#from core.logs.failedLog import failed_log
import time
from core.data_cleaning.DataCleaning import DataCleaning


# 태그 관련 함수 제작
# 고해상도의 이미지 링크를 얻기 위한 작업이 복잡해
# 별도의 get_image 함수로 분류
# 번들 중에 게임 이름이 제일 짧

def find_bundle(driver, driver_eng):
    bundleList = []
    tmp_title = ''
    tmp_url = ''
    try:
        bundleList = driver.find_element(By.CSS_SELECTOR,"section[aria-label='이 번들']").find_element(By.CSS_SELECTOR, "div[class='ModuleRow-module__row___N1V3E']").find_element(By.CSS_SELECTOR, "ol[class='ItemsSlider-module__wrapper___nAi6y']").find_elements(By.TAG_NAME, 'li')

        bundleList.pop()
        print(bundleList)
        
        print(len(bundleList))
        for titles in bundleList:
            title = titles.find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME,'a').get_attribute('title')
            link = titles.find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME,'a').get_attribute('href')


            title = title.replace('Xbox Series X|S용 ','').replace('Xbox One용 ','').replace(' Xbox One', '').replace(' Xbox Series X|S','')

            print(title)
            if tmp_title == '':
                tmp_title = title
                tmp_url = link
                

            elif len(title) < len(tmp_title):
                
                tmp_title = title
                tmp_url = link
            
            print(tmp_title)
            
        print(tmp_title)
        print(tmp_url)
        driver.get(tmp_url)
        driver_eng.get(tmp_url.replace('ko-KR', 'en-us'))
        time.sleep(10)
        
        
        
    except NoSuchElementException:
        print("this is not bundle")
        
        return None

def get_tag(driver):
    ele = driver.find_element(By.CSS_SELECTOR, "div[class='typography-module__xdsSubTitle1___N02-X ProductInfoLine-module__productInfoLine___Jw2cv']")
    tagRaw = ele.find_element(By.TAG_NAME, "span").text
    
    tagRaw = tagRaw.replace('및', '•').replace(' ','')
    
    tagList = tagRaw.split('•')
    
    del tagList[0]
    
    #print(tagList)
    return tagList
    
    
    
    
def get_image(driver):
    imgList = []
    
    #wait = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='ItemsSlider-module__arrowButton___ZH7Ek commonStyles-module__basicButton___go-bX Button-module__iconButtonBase___uzoKc Button-module__basicBorderRadius___TaX9J Button-module__sizeIconButtonMedium___WJrxo Button-module__buttonBase___olICK Button-module__textNoUnderline___kHdUB Button-module__typeBrand___MMuct Button-module__overlayModeSolid___v6EcO']")))
    wait = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ol[class='ItemsSlider-module__wrapper___nAi6y']")))
    
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
    
    dc = DataCleaning('xbox')
    
    autokwd = list()
    
    driver.implicitly_wait(10)
    driver_eng.implicitly_wait(10)
    
    
    driver.get(url)
    driver_eng.get(url_eng)
    
    
    find_bundle(driver,driver_eng)
    
    title = driver.find_element(By.CSS_SELECTOR, "h1[data-testid='ProductDetailsHeaderProductTitle']").text
    
    
    
    try:
        engTitle = driver_eng.find_element(By.CSS_SELECTOR, "h1[data-testid='ProductDetailsHeaderProductTitle']").text
    except NoSuchElementException:
        engTitle = title


    autokwd.append(dc.cleanKeyword(engTitle))
    autokwd.append(dc.cleanKeyword(title))
    
    
    
    autokwd = sorted(set(autokwd), key= lambda x: autokwd.index(x))
    
    
        
    description = driver.find_element(By.CSS_SELECTOR, "p[class='Description-module__description___ylcn4 typography-module__xdsBody2___RNdGY ExpandableText-module__container___Uc17O']").text
    company = driver.find_element(By.CSS_SELECTOR, "div[class='typography-module__xdsBody2___RNdGY']").text
    tagList = get_tag(driver)
    screenList = get_image(driver)
    
    try:
        thum = driver.find_element(By.CSS_SELECTOR, "img[class='ProductDetailsHeader-module__backgroundImage___34Nro img-fluid']").get_attribute('src')
    except NoSuchElementException:
        thum = screenList[0]
        
    
    detail_dict = {
        'imageurl': thum,
        'description': description,
        'autokwd': ",".join(autokwd),
        'company': company,
        'screenshot': ",".join(screenList),
        'tag':",".join(tagList),
        'platform': 'xbox'
    }
    
    
    
    print(detail_dict)
    
    return detail_dict