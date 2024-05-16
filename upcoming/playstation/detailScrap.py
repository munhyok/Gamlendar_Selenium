from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from core.data_cleaning.DataCleaning import DataCleaning
from core.logs.failedLog import failed_log

LOADING_PAGE = 2


# playstation은 스크린샷이 따로 존재하지 않아서
# 스크린샷은 썸네일 이미지로 대체


def detail_scrap(driver, driver_eng, url, url_eng):
    
    dc = DataCleaning('playstation')
    
    autokwd = list()
    adultTag = ['성인']
    
    screenList = []
    
    driver.get(url)
    driver_eng.get(url_eng)
    
    tags = driver.find_element(By.CSS_SELECTOR, "dd[data-qa='gameInfo#releaseInformation#genre-value']").text
    tagList = tags.split(',')
    
    
    
    
    thum = driver.find_element(By.XPATH, '/html/body/div[3]/main/div/div[1]/div[1]/div/div/div/div/span/img[2]').get_attribute('src')
    description = driver.find_element(By.CSS_SELECTOR, "div[class='psw-l-w-1/1 psw-l-w-2/3@tablet-s psw-l-w-2/3@tablet-l psw-l-w-1/2@laptop psw-l-w-1/2@desktop psw-l-w-1/2@max']").find_element(By.TAG_NAME, 'p').text
    company = driver.find_element(By.CSS_SELECTOR, "dd[data-qa='gameInfo#releaseInformation#publisher-value']").text
    releaseDate = driver.find_element(By.CSS_SELECTOR, "dd[data-qa='gameInfo#releaseInformation#releaseDate-value']").text
    
    # 한국에는 출시하지만 미국에선 출시하지 않을 때의 예외 처리
    try:
        engTitle = driver_eng.find_element(By.CSS_SELECTOR, "h1[data-qa='mfe-game-title#name']").text
        
    except NoSuchElementException:
        engTitle = None
    
    
    title = driver.find_element(By.CSS_SELECTOR, "h1[data-qa='mfe-game-title#name']").text
    
    
    
    
    
    if engTitle != None:
        autokwd.append(dc.cleanKeyword(engTitle))
    
    autokwd.append(dc.cleanKeyword(title))
        
    autokwd = sorted(set(autokwd), key=lambda x: autokwd.index(x))
    screenList.append(thum)
    
    for adult in adultTag:
        if adult in tagList:
            print("adult game")
            
            failed_log(True,title,'filtering Adult game','playstation')

            detail_dict = {
                'date': dc.formatDate(releaseDate),
                'imageurl': '',
                'description': "Adult Game",
                'autokwd': '',
                'company': "",
                'screenshot': '',
                'tag':'',
                'platform': "playstation"
            }
            
            print(detail_dict)
            return detail_dict
        
    
    detail_dict = {
        'date': dc.formatDate(releaseDate),
        'imageurl': thum,
        'description': description,
        'autokwd': ",".join(autokwd),
        'company': company,
        'screenshot': ",".join(screenList),
        'tag':",".join(tagList),
        'platform': "playstation"
    }
    
    print(detail_dict)
    
    return detail_dict
        
        
        
    
    
    