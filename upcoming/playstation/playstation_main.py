import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from upcoming.steam.scrollScrap import scroll_scrap
from upcoming.steam.detailScrap import detail_scrap, pass_adult
from core.data.concatData import concat_data
from core.logs.failedLog import failed_log
from selenium import webdriver
from datetime import datetime

NOW = time.time()
LOADING_PAGE = 2

DATE = datetime.fromtimestamp(NOW).strftime('%Y-%m-%d %H:%M:%S')

def playstation_upcoming(driver, driver_english):
    
    pageCount = 0
    
    driver.get('https://store.playstation.com/ko-kr/pages/browse/1?next_thirty_days=conceptReleaseDate')
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_selected((By.XPATH, '/html/body/div[3]/main/div/section/div/div/div/div[2]/div[2]/ul')))
    
    
    count = driver.find_element(By.CLASS_NAME, 'psw-t-body.psw-c-t-2').text
    count = int(count[:3].replace('/',''))
    
    # count = 26
    # 한 페이지에 24개의 게임 타이틀 노출
    # 

    # count가 0으로 딱 떨어지지 않은 경우는 전부 pageCount에 + 1
    
    if count % 24 == 0:
        pageCount = int(count / 24)
    else: pageCount = int(count / 24) + 1
    
    print(f'페이지 수 {pageCount}')
    print('게임 수집 시작')
    
    
    
    

    
    
        
    
    
    
    


    