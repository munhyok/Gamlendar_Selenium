import time
import os
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from datetime import datetime

from dotenv import load_dotenv
from upcoming.xbox.pageScrap import page_scrap
from upcoming.xbox.detailScrap import detail_scrap

load_dotenv()

#driver = webdriver.Chrome()
# 설계 정리
# xbox는 게관위의 등급분류 시스템을 거친 게임을 가져오기 때문에
# 등급이 없는 게임은 웬만해서 등록 안하는 것 같기 때문에
# 별도의 성인게임 필터링은 필요없을듯...?
# 
# 플로우
# 로그인 -> upcoming 페이지 -> 상세 페이지 -> 이름, 설명, 스크린샷, 태그(x)
# 디럭스, Deluxe, 프리미엄, Premium, 얼티밋, Ultimate, 컴플리트, Complete, 디피니티브, Definitive, 
# 위 에디션 물품은 제외시켜서..

# 그냥 Edition 키워드를 가져다가 필터링 거치면 되지않을까?
# 라고 고민했지만 생각보다 Edition이란 게임이 뒤에 들어가는 게임도 많고
# 뭔가 게임 패키지가 꼬여있다...

def xbox_login(driver):
    xbox_account = os.getenv('XBOXACCOUNT')
    xbox_password = os.getenv('XBOXPASSWORD')
    
    def login_action():
        account = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        account.click()
        account.send_keys(xbox_account)
        account.send_keys(Keys.ENTER)

        time.sleep(3)
        password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password.click()
        password.send_keys(xbox_password)
        password.send_keys(Keys.ENTER)
        
        
        time.sleep(3)
        loginState = driver.find_element(By.CSS_SELECTOR, "input[id='idBtn_Back']")
        loginState.click()
        

    driver.get("https://www.xbox.com/ko-kr/games/all-games?cat=upcoming")
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'mectrl_topHeader').click()
    
    driver.implicitly_wait(10)
    
    try:
        login_action()
        time.sleep(5)
    except:
        driver.find_element(By.CLASS_NAME, 'mectrl_topHeader').click()
        time.sleep(5)
        login_action()
        
        
    driver.implicitly_wait(10)
        

def xbox_upcoming(driver, driver_eng):
    gameList = []
    detailList = []
    xbox_login(driver)
    pageList = driver.find_element(By.CSS_SELECTOR, "button[id='unique-id-for-paglist-generated-select-menu-trigger']")
    pageList.click()
    time.sleep(0.5)
    menu = driver.find_element(By.CSS_SELECTOR, "li[id='unique-id-for-paglist-generated-select-menu-3']")
    menu.click()
    print("Xbox Login Complete")
    
    gameList = page_scrap(driver)
    
    for count in range(len(gameList)):
        kor = gameList[count]['url']
        eng = gameList[count]['url'].replace('ko-kr','en-us')
        
        result = detail_scrap(driver, driver_eng, kor, eng)
        detailList.append(result)
        
    
        
    
    
    



