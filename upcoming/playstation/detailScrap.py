from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

from core.logs.failedLog import failed_log

LOADING_PAGE = 2


# playstation은 스크린샷이 따로 존재하지 않아서
# 스크린샷은 썸네일 이미지로 대체


def detail_scrap(driver, driver_eng, url, url_eng):
    
    adultTag = ['성인']
    autokwdSet = set()
    screenList = []
    
    driver.get(url)
    driver_eng.get(url_eng)
    
    tags = driver.find_element(By.CSS_SELECTOR, "dd[data-qa='gameInfo#releaseInformation#genre-value']").text
    tagList = tags.split(',')
    
    
    
    
    thum = driver.find_element(By.XPATH, '/html/body/div[3]/main/div/div[1]/div[1]/div/div/div/div/span/img[2]').get_attribute('src')
    description = driver.find_element(By.CSS_SELECTOR, "div[class='psw-l-w-1/1 psw-l-w-2/3@tablet-s psw-l-w-2/3@tablet-l psw-l-w-1/2@laptop psw-l-w-1/2@desktop psw-l-w-1/2@max']").find_element(By.TAG_NAME, 'p').text
    company = driver.find_element(By.CSS_SELECTOR, "dd[data-qa='gameInfo#releaseInformation#publisher-value']").text
    releaseDate = driver.find_element(By.CSS_SELECTOR, "dd[data-qa='gameInfo#releaseInformation#releaseDate-value']").text
    
    
    title = driver.find_element(By.CSS_SELECTOR, "h1[data-qa='mfe-game-title#name']").text
    autokwdSet.add(title)
    # 한국에는 출시하지만 미국에선 출시하지 않을 때의 예외 처리
    try:
        engTitle = driver_eng.find_element(By.CSS_SELECTOR, "h1[data-qa='mfe-game-title#name']").text
        autokwdSet.add(engTitle)
    except NoSuchElementException:
        engTitle = None
        
        
    autokwd = list(autokwdSet)
    screenList.append(thum)
    
    for adult in adultTag:
        if adult in tagList:
            print("adult game")
            
            failed_log(True,title,'filtering Adult game','playstation')

            detail_dict = {
                'imageurl': '',
                'description': "Adult Game",
                'autokwd': [],
                'company': "",
                'screenshot': [],
                'tag':[],
                'platform': []
            }
            
            return detail_dict
        
    
    detail_dict = {
        'imageurl': thum,
        'description': description,
        'autokwd': autokwd,
        'company': company,
        'screenshot': screenList,
        'tag':tagList,
        'platform': ["playstation"]
    }
    
    print('-'*20)
    print(tags)
    print(thum)
    print(company)
    print(description)
    print(releaseDate)
    print()
    print(title)
    print(engTitle)
    
    return detail_dict
        
        
        
    
    
    