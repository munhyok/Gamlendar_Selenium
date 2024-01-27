from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from core.logs.failedLog import failed_log

# 수집 전략
# 전체 페이지 수집 -> 오래 걸리지만 플랫폼 특성상 게임 정보가 많으면 굳..이라고 생각했지만
# 전체 페이지 수집이 3800개가 넘는다. 걍 100개씩 수집하자.. 과거 데이터는 포기
# 중복 데이터 처리 방법..은 SQL에 있는 UNIQUE를 사용하면 되지 않을까..? 게임 이름에 unique 적용
# 


def page_scrap(driver, driver_eng):
    filter_words = ['Hentai'] # 성인게임 필터링
    pageList = list()
    
    
    games = driver.find_elements(By.CLASS_NAME, 'category-product-item')
    
    
    for game in games[:101]:
        
        title = game.find_element(By.CLASS_NAME, 'category-product-item-title-link').text
        url = game.find_element(By.CLASS_NAME, 'category-product-item-title-link').get_attribute('href')
        
        if filter_words[0] not in title:
        
            pageGame = {
                'title': title,
                'url': url,

            }
            
        pageList.append(pageGame)
        
    
        
    print(pageList)
    print(len(pageList))
    
    return pageList
