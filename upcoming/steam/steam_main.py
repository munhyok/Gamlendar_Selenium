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

# 전략
# 출시 게임을 전부하기엔 게임의 수가 너무 많고 (약 4000개)
# 성인 게임을 제대로 필터링하지 못할 것 같다라는 판단에 일단 인기 찜 목록(약 2100개)부터 수집한다.
# 최대한 보수적으로 데이터 수집 *성인게임 수집 금지...
# listup -> detail game data -> POST DB
# 추후 출시 날짜가 변경될 수도 있으니 DB 이용해야할까...?
# pandas로 정리 CONCAT -> postgreSQL 테이블 추가
# (데이터 관리 추후 관리자 페이지가 필요할 것 같아서.. 미리 작업)
# 

NOW = time.time()
LOADING_PAGE = 2

DATE = datetime.fromtimestamp(NOW).strftime('%Y-%m-%d %H:%M:%S')


def steam_upcoming(driver, driver_eng):
    
    detailList = []
    
    
    # 인기 찜 목록
    driver.get("https://store.steampowered.com//search/?supportedlang=koreana%2Cenglish&category1=998&filter=popularwishlist&ndl=1")
    driver.execute_script('ChangeLanguage("koreana")')
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[1]/div[7]/div[6]/div/div[2]/h2"),"인기 찜 목록"))
    
    print("Text Changed, Scroll Down Start")
    time.sleep(1)
    
    
    gameList = scroll_scrap(driver)
    
    
    print('성인 인증 페이지')
    pass_adult(driver, driver_eng)
    
    print('detail scrap start')
    for i in range(len(gameList)):
        result = detail_scrap(driver, driver_eng, gameList[i]['url'])
        
        if result != None:
            detailList.append(result)
        
        
    failedList = failed_log(False, None, None, None)
        
    concat_data(gameList, detailList, DATE)
    
    
    
    time.sleep(5)
    
    
    f = open('./upcoming/steam/log/'+DATE+'_failed_log.txt','w')
    for i in failedList:
        data = "%s\n" % i
        f.write(data)
    f.close()
    
    
    
    
    # 수집 데이터 TEST 저장 실제로 사용할 땐 없앨 예정
    f = open('./test/test.txt','w')
    for i in gameList:
        data = "%s\n" % i
        f.write(data)
    f.close()
    
    f = open('./test/test_detail.txt','w')
    for i in detailList:
        data = "%s\n" % i
        f.write(data)
    f.close()