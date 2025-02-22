from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from core.logs.failedLog import failed_log
from core.Webdriver import Webdriver

FILTERWORDS = [
    '디럭스','Deluxe',
    '프리미엄','Premium',
    '얼티밋','Ultimate',
    '얼티메이트',
    '컴플리트', 'Complete',
    '디피니티브', 'Definitive',
    '다운로드', 'Download',
    '스페셜', 'Special',
    '번들', 'Bundle',
    '애드온', 'Add-On',
    '파운더스', 'Founders'
    
    ]

def page_scrap():
    wd = Webdriver()
    
    gameList = []
    wait = WebDriverWait(wd.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='gameDivLink']")))
    print('Loading Done, Scrap start')
    
    games = wd.driver.find_elements(By.CSS_SELECTOR, "div[class='m-product-placement-item f-size-medium context-game gameDiv']")
    
    for game in games:
        filterCheck = False
        
        title = game.find_element(By.CSS_SELECTOR, "h3[itemprop='product name']").text
        url = game.find_element(By.TAG_NAME, 'a').get_attribute('href')              
        releaseDate = game.get_attribute('data-releasedate')
        releaseDate = releaseDate[:10]
        
        for word in FILTERWORDS:
            if word in title:
                filterCheck = True
                 
        if filterCheck == False:
            
            pageGame = {
                'title': title,
                'url': url,
                'date': releaseDate
            }
            
            gameList.append(pageGame)
        else: 
            failed_log(True, title, "Detected Filter Words", "xbox")
            
        
            
    print(gameList)
    return gameList
            
            

            
                
                
             
    
    
    