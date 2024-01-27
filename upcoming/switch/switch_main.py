import time
import os
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from datetime import datetime

from core.logs.failedLog import failed_log
from core.data.concatData import concat_data

from upcoming.switch.pageScrap import page_scrap
from upcoming.switch.detailScrap import detail_scrap

NOW = time.time()
DATE = datetime.fromtimestamp(NOW).strftime('%Y-%m-%d %H:%M:%S')




def popup_close(driver): #팝업 닫기 함수
    
    wait = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='popup-close']")))
    popupClose = driver.find_element(By.CSS_SELECTOR, "button[class='popup-close']")
    popupClose.click()
    
    print('popup closed')

def switch_upcoming(driver, driver_eng):
    gameList = []
    detailList = []
    
    driver.get("https://store.nintendo.co.kr/games/all-released-games")

    popup_close(driver)
    
    
    #여기부터 코드 작성
    gameList = page_scrap(driver,None)
    
    for count in range(len(gameList)):
        
        result = detail_scrap(driver,None,gameList[count]['url'],None)
        detailList.append(result)
        
    
    failedList = failed_log(False, None, None, 'switch')
        
    concat_data(gameList, detailList, DATE, 'switch')
    
    f = open('./upcoming/switch/log/'+DATE+'_failed_log.txt','w')
    for i in failedList:
        data = "%s\n" % i
        f.write(data)
    f.close()   
    
    
    
    
    