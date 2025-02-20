import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from upcoming.playstation.pageScrap import page_scrap
from upcoming.playstation.detailScrap import detail_scrap
from core.data.concatData import concat_data
from core.logs.failedLog import failed_log
from core.Webdriver import Webdriver
from datetime import datetime


LOADING_PAGE = 2

NOW = time.time()
DATE = datetime.fromtimestamp(NOW).strftime('%Y-%m-%d %H:%M:%S')

def playstation_upcoming():
    wd = Webdriver()
    
    
    
    detailList = list()
    pageCount = 0
    
    wd.driver.get('https://store.playstation.com/ko-kr/category/82ced94c-ed3f-4d81-9b50-4d4cf1da170b/1')
    
    wait = WebDriverWait(wd.driver, 10)
    
    
    time.sleep(LOADING_PAGE)
    count = wd.driver.find_element(By.CLASS_NAME, 'psw-t-body.psw-c-t-2').text
    count = count.split('개')
    count = count[0]
    count = int(count)
    
    
    print(count)
    
    # 한 페이지에 최대 24개의 게임 타이틀 노출
    if count % 24 == 0: # count가 0으로 딱 떨어지지 않은 경우는 전부 pageCount에 + 1
        pageCount = int(count / 24)
    else: pageCount = int(count / 24) + 1
    
    print(f'페이지 수 {pageCount}')
    print(f'총 {count}개 게임 수집 시작')
    
    
    gameList = page_scrap(pageCount)
    
    for i in range(0, len(gameList)):
        result = detail_scrap(gameList[i]['url'], gameList[i]['url'].replace('ko-kr','en-us'))
        detailList.append(result)
    
    failedList = failed_log(False, None, None, 'playstation')
        
    concat_data(gameList, detailList, DATE, 'playstation')
    
    f = open('./upcoming/playstation/log/'+DATE+'_failed_log.txt','w')
    for i in failedList:
        data = "%s\n" % i
        f.write(data)
    f.close()    
    
    

    
    
        
    
    
    
    


    