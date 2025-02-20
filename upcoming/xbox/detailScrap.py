from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
#from core.logs.failedLog import failed_log
import time
from core.data_cleaning.DataCleaning import DataCleaning
from core.Webdriver import Webdriver


def find_bundle(driver, driver_eng):
    isBundle = False
    bundleList = None
    
    try:
        
        bundleText = driver.find_element(By.CSS_SELECTOR, "section[aria-label='이 번들']").get_attribute("aria-label")
        
        if bundleText == '이 번들':
            isBundle = True
            print("find bundle")
            
            
        if isBundle:
            bundleList = driver.find_element(By.CSS_SELECTOR, "section[aria-label='이 번들']").find_element(By.CSS_SELECTOR, "div[class='ModuleRow-module__row___N1V3E']").find_element(By.CSS_SELECTOR, "ol[class='ItemsSlider-module__wrapper___nAi6y']").find_elements(By.TAG_NAME, "li")
            print(len(bundleList))
            
            for i in range(len(bundleList)):
                bundleSector = bundleList[i].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME, 'a')
                try:
                    info = bundleSector.find_element(By.CSS_SELECTOR, "div[class='ProductCard-module__infoBox___M5x18']").find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'span').text
                except:
                    info = bundleSector.find_element(By.CSS_SELECTOR, "div[class='ProductCard-module__infoBox___M5x18']").find_element(By.CSS_SELECTOR, "span[class='typography-module__xdsBody2___RNdGY']").text
                    
                if info != '추가 기능 보기': # 얘는 오리지널 게임이 무조건 아닙니다.
                    
                    if info != '게임 보기': # 게임 보기 + 가격 같은 동시에 존재할 가능성이 있기 때문에 넣은 조건문
                        kor = bundleList[i].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME, 'a').get_attribute("href")
                        eng = kor.replace('ko-KR', 'en-us')
                        
                        print(eng)
                    
                        driver.get(kor)
                        driver_eng.get(eng)
                        return None
                    
                    kor = bundleList[i].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME, 'a').get_attribute("href")
                    eng = kor.replace('ko-KR', 'en-us')
                    
                    print(eng)
                
                    driver.get(kor)
                    driver_eng.get(eng)
                    return None
            
    except NoSuchElementException:
        print("can't find bundle area")
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
    
    
    wait = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ol[class='ItemsSlider-module__wrapper___nAi6y']")))
    
    gallery = driver.find_element(By.CSS_SELECTOR, "section[aria-label='갤러리']").find_element(By.CSS_SELECTOR, "div[class='ModuleRow-module__row___N1V3E']").find_elements(By.CSS_SELECTOR, "ol[class='ItemsSlider-module__wrapper___nAi6y']")
    
    
    imgClick = gallery[0].click()
    time.sleep(0.5)
    
    imgNumber = driver.find_element(By.CSS_SELECTOR, "h2[class='typography-module__xdsSubTitle1___N02-X']").text
    
    imgNumber = imgNumber[13:]
    imgNumber = int(imgNumber[:-1])
    
    
    
    
    for _ in range(0, imgNumber):
        
        try:
            img = driver.find_element(By.CSS_SELECTOR,"div[class='MediaViewer-module__viewMedia___5xlQv']").find_element(By.CSS_SELECTOR, "img[class='WrappedResponsiveImage-module__image___QvkuN MediaItem-module__image___VlVzn']").get_attribute('src')
            imgList.append(img)
        except:
            pass
        time.sleep(1)
        nextBtn = driver.find_element(By.CSS_SELECTOR, "button[class='glyphs-module__glyph-prepend___3JVuT glyphs-module__glyph-prepend-chevron-right___i5kNz MediaViewerSlider-module__arrowButton___pc-7m Button-module__basicBorderRadius___TaX9J Button-module__defaultBase___c7wIT Button-module__buttonBase___olICK Button-module__textNoUnderline___kHdUB Button-module__typeTertiary___wNh6R Button-module__sizeMedium___T+8s+ Button-module__overlayModeSolid___v6EcO']")
        nextBtn.click()
    
    #print(imgNumber)
    #print(imgList)
    return imgList



def detail_scrap(url, url_eng):
    wd = Webdriver()
    
    dc = DataCleaning('xbox')
    
    autokwd = list()
    
    wd.driver.implicitly_wait(10)
    wd.driver_eng.implicitly_wait(10)
    
    
    wd.driver.get(url)
    wd.driver_eng.get(url_eng)
    
    
    find_bundle(wd.driver,wd.driver_eng)
    
    title = wd.driver.find_element(By.CSS_SELECTOR, "h1[data-testid='ProductDetailsHeaderProductTitle']").text
    
    
    
    try:
        engTitle = wd.driver_eng.find_element(By.CSS_SELECTOR, "h1[data-testid='ProductDetailsHeaderProductTitle']").text
    except NoSuchElementException:
        engTitle = title


    autokwd.append(dc.cleanKeyword(engTitle))
    autokwd.append(dc.cleanKeyword(title))
    
    
    
    autokwd = sorted(set(autokwd), key= lambda x: autokwd.index(x))
    
    
        
    description = wd.driver.find_element(By.CSS_SELECTOR, "p[class='Description-module__description___ylcn4 typography-module__xdsBody2___RNdGY ExpandableText-module__container___Uc17O']").text
    company = wd.driver.find_element(By.CSS_SELECTOR, "div[class='typography-module__xdsBody2___RNdGY']").text
    tagList = get_tag(wd.driver)
    screenList = get_image(wd.driver)
    
    try:
        thum = wd.driver.find_element(By.CSS_SELECTOR, "img[class='ProductDetailsHeader-module__backgroundImage___34Nro img-fluid']").get_attribute('src')
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