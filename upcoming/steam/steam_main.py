import time
import os
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


from dotenv import load_dotenv
from upcoming.steam.scrollScrap import scroll_scrap
from upcoming.steam.detailScrap import detail_scrap, pass_adult
from core.Webdriver import Webdriver
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
# pandas로 정리 CONCAT -> MariaDB 테이블 추가
# (데이터 관리 추후 관리자 페이지가 필요할 것 같아서.. 미리 작업)
# 


load_dotenv()

NOW = time.time()
LOADING_PAGE = 2

DATE = datetime.fromtimestamp(NOW).strftime('%Y-%m-%d %H:%M:%S')

def steam_login(driver, language):
    
    steam_account = os.getenv('STEAM_ACCOUNT')
    steam_account_eng = os.getenv('STEAM_ACCOUNT_ENG')
    steam_password = os.getenv('STEAM_PASSWORD')
    
    login_url = 'https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_4__global-header'
    
    driver.get(login_url)
    
    time.sleep(5)
    
    account = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
    
    
    account.click()
    if language == 'kor':
        account.send_keys(steam_account)
    else: account.send_keys(steam_account_eng)
    time.sleep(3)
    
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    password.click()
    password.send_keys(steam_password)
    password.send_keys(Keys.ENTER)
    
    time.sleep(10)
    
    
    
    
    
    
    
    
    

def steam_upcoming():
    
    detailList = []
    wd = Webdriver()

    
    
    steam_login(wd.driver, 'kor')
    steam_login(wd.driver_eng, 'eng')
    
    # 인기 찜 목록
    wd.driver.get("https://store.steampowered.com/search/?category1=998&os=win&supportedlang=english&filter=comingsoon&ndl=1")
    wd.driver.execute_script('ChangeLanguage("koreana")')
    
    time.sleep(5)
    wd.driver.get("https://store.steampowered.com/search/?category1=998&os=win&supportedlang=english&filter=comingsoon&ndl=1")
    
    wait = WebDriverWait(wd.driver, 10)
    wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[1]/div[7]/div[6]/div[3]/div[2]/h2"),"출시 예정"))
    
    print("Text Changed, Scroll Down Start")
    time.sleep(1)
    
    
    gameList = scroll_scrap()
    
    
    print('성인 인증 페이지')
    pass_adult()
    
    print('detail scrap start')
    gameListLength = len(gameList)
    for i in range(gameListLength):    
        try:
            result = detail_scrap(gameList[i]['url'])
        except:
            wd.quitDriver()
            
            wd.restartDriver()
            time.sleep(5)
            steam_login(wd.driver, 'kor')
            steam_login(wd.driver_eng, 'eng')
            time.sleep(5)
            pass_adult()
            result = detail_scrap(gameList[i]['url'])
            
        if result != None:
            detailList.append(result)
            
        print(f"{i}/{gameListLength} - {gameList[i]['title']}")
        #time.sleep(2)
        
        
    failedList = failed_log(False, None, None, 'pc')
        
    concat_data(gameList, detailList, DATE, 'steam')
    
    time.sleep(5)
    
    
    f = open('./upcoming/steam/log/'+DATE+'_failed_log.txt','w')
    for i in failedList:
        data = "%s\n" % i
        f.write(data)
    f.close()
    
    

    
    
    # 수집 데이터 TEST 저장 실제로 사용할 땐 없앨 예정
    #f = open('./test/test.txt','w')
    #for i in gameList:
    #    data = "%s\n" % i
    #    f.write(data)
    #f.close()
    #
    #f = open('./test/test_detail.txt','w')
    #for i in detailList:
    #    data = "%s\n" % i
    #    f.write(data)
    #f.close()