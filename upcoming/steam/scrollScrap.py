from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


LOADING_PAGE = 2

def scroll_scrap(driver):
    gameList = list()
    doScroll = True
    
    oldPageHeight = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    
    while(doScroll):
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(LOADING_PAGE)
        
        newPageHeight = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
        
        
        

        if oldPageHeight == newPageHeight:
            doScroll = False
            print("Page End")
            break

        oldPageHeight = newPageHeight
        
        
        
        gameRows = driver.find_element(By.ID, 'search_resultsRows')
        games = gameRows.find_elements(By.TAG_NAME, 'a')

        for i in range(len(gameList),len(games)):
            title = games[i].find_element(By.CLASS_NAME, 'title').text
            url = games[i].get_attribute('href')
            releaseDate = games[i].find_element(By.CLASS_NAME, 'col.search_released.responsive_secondrow').text

            my_game = {
                'title': title,
                'url': url,
                'date': releaseDate


            }
            gameList.append(my_game)

        print(len(gameList))
    return gameList