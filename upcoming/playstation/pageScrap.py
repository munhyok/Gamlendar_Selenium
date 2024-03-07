from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from core.data_cleaning.DataCleaning import DataCleaning
import time

LOADING_PAGE = 2

def page_scrap(driver, driver_english, pageNumber):
    
    dc = DataCleaning('playstation')
    pageList = list()
    
    for _ in range(1, pageNumber+1):
        time.sleep(LOADING_PAGE)
        
        gameGrid = driver.find_element(By.CLASS_NAME, 'psw-grid-list.psw-l-grid')
        
        games = gameGrid.find_elements(By.TAG_NAME, 'li')
        
        for game in games:
            
            title = game.find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME,'section').find_element(By.CLASS_NAME, 'psw-t-body.psw-c-t-1.psw-t-truncate-2.psw-m-b-2').text
            url = game.find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'a').get_attribute('href')

            pageGame = {
                'title': dc.cleanKeyword(title),
                'url': url,
                
            }
            
            pageList.append(pageGame)
        
        print(pageList)
        
        
        nextBtn = driver.find_element(By.CLASS_NAME, 'psw-icon.psw-icon--chevron-right.psw-icon.psw-icon-size-2.psw-icon--chevron-right').click()
        print('nextBtn clicked!')
        
            
        
        return pageList
        
        