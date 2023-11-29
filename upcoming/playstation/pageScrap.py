from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

LOADING_PAGE = 2

def page_scrap(driver, driver_english, pageNumber):
    
    pageList = list()
    
    for _ in range(1, pageNumber+1):
        time.sleep(LOADING_PAGE)
        
        gameGrid = driver.find_element(By.CLASS_NAME, 'psw-grid-list.psw-l-grid')
        
        games = gameGrid.find_elements(By.TAG_NAME, 'li')
        
        for game in games:
            
            title = game.find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME,'section').find_element(By.CLASS_NAME, 'psw-t-body.psw-c-t-1.psw-t-truncate-2.psw-m-b-2').text
            url = game.find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'a').get_attribute('href')

            pageGame = {
                'title': title,
                'url': url,
                
            }
            
            pageList.append(pageGame)
        
        print(pageList)
        
        nextBtn = driver.find_element(By.XPATH, '/html/body/div[3]/main/div/section/div/div/div/div[2]/div[2]/div/nav/button[2]/span').click()
        print('nextBtn clicked!')
        
            
        
        return pageList
        
        