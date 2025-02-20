from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from core.data_cleaning.DataCleaning import DataCleaning
from core.Webdriver import Webdriver
import time


# 스크롤하고 데이터 파싱까지 합니다 :)

# 페이지가 좀 많아지면 위가 짤리는 경우가 많아
# 페이지 하단으로 이동 -> 로딩 후 데이터를 가져오는 방식
# 게임의 수가 많아도 상관없이 크롤링 가능
# 

LOADING_PAGE = 2 # 데이터 로딩 2초

def scroll_scrap():
    wd = Webdriver()
    dc = DataCleaning('steam')
    
    gameList = list()
    doScroll = True
    
    currentPageHeight = wd.driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    
    while(doScroll):
        
        wd.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(LOADING_PAGE)
        
        newPageHeight = wd.driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

        if currentPageHeight == newPageHeight:
            doScroll = False
            print("Page End")
            break

        currentPageHeight = newPageHeight
        
        
        gameRows = wd.driver.find_element(By.ID, 'search_resultsRows')
        games = gameRows.find_elements(By.TAG_NAME, 'a')

        for i in range(len(gameList),len(games)):
            title = games[i].find_element(By.CLASS_NAME, 'title').text
            url = games[i].get_attribute('href')
            releaseDate = games[i].find_element(By.CLASS_NAME, 'col.search_released.responsive_secondrow').text

            pageGame = {
                'title': title,
                'url': url,
                'date': dc.formatDate(releaseDate)


            }
            gameList.append(pageGame)

        print(len(gameList))
        
    return gameList