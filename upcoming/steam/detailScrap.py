from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from core.logs.failedLog import failed_log

from core.Webdriver import Webdriver
from core.data_cleaning.DataCleaning import DataCleaning
from core.Webdriver import Webdriver
import time


# 수집 목록
# Thum, description, company, tag, screenshot, english name
# 한국어, 영어 별도로 driver를 만들어서 2개 돌려야 수집 속도가 올라갈듯..
# try accept를 사용하고 싶지만
# 무지성으로 사용하면 코드가 더러워보여서.. 최대한 통제 가능한 부분은 None으로 처리



def pass_adult():
    # 한 번만 인증하면 되기 때문에 GTA5에서 미리 인증을 거치고
    # 추후 게임 데이터 수집을 시작
    
    wd = Webdriver()
    
    wd.driver.get('https://store.steampowered.com/agecheck/app/271590/')
    wd.driver_eng.get('https://store.steampowered.com/agecheck/app/271590/')

    try:
        time.sleep(1)
        wd.driver.find_element(By.ID, 'ageYear').click()
        wd.driver_eng.find_element(By.ID, 'ageYear').click()
        time.sleep(0.5)


        wd.driver.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[6]/div[3]/div[2]/div/div[1]/div[2]/select[3]/option[63]').click()
        wd.driver_eng.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[6]/div[3]/div[2]/div/div[1]/div[2]/select[3]/option[63]').click()


        time.sleep(0.5)
    except: pass
    
    wd.driver.find_element(By.ID, 'view_product_page_btn').click()
    wd.driver_eng.find_element(By.ID, 'view_product_page_btn').click()

    time.sleep(3)
    
    


    
    


def detail_scrap(url):
    
    
    dc = DataCleaning('steam')
    wd = Webdriver()
    # 이 태그가 들어간 친구들은 수집 금지
    adultTag = ['헨타이','후방주의','선정적인 내용',]
    
    autokwd = list()
    screenList = []
    tagList = []
    detailList = []
    
    
    
    wd.driver.implicitly_wait(10)
    wd.driver_eng.implicitly_wait(10)
    
    wd.driver.get(url)
    wd.driver_eng.get(url)

    
    # 태그 수집
    try:
        tags = wd.driver.find_element(By.CLASS_NAME, 'glance_tags.popular_tags').find_elements(By.CLASS_NAME,'app_tag')
        for tag in tags:
            plain = tag.text
            if not plain == '':
                tagList.append(plain)
        tagList.remove('+')
    except NoSuchElementException:
        
        tagList.append("-")
        

        
    
    
 
    try:       
        title = wd.driver.find_element(By.ID, 'appHubAppName').text
    except: 
        title = ''
    
    for adult in adultTag:
        if adult in tagList:
            print("adult game")
            
            failed_log(True,title,'filtering Adult game','pc')
            
            detail_dict = {
                'imageurl': '',
                'description': "Adult Game",
                'autokwd': 'Adult Game',
                'company': "",
                'screenshot': '',
                'tag':'',
                'platform': 'steam'
            }
            
            return detail_dict
    
    if title == '(Old steam page)':
        # 사실 Old steam page는 개발자가 그렇게 만든 페이지 같아서 나중에 별도로 예외처리를 만들어야함
        print("Old Steam Page")
        
        detail_dict = {
                'imageurl': '',
                'description': "Old Steam Page",
                'autokwd': 'Adult Game',
                'company': "",
                'screenshot': '',
                'tag':'',
                'platform': 'steam'
        }
        
        return detail_dict
    
    # 썸네일, 개발사
    try:
        thum = wd.driver.find_element(By.CLASS_NAME, 'game_header_image_full').get_attribute('src')
        company = wd.driver.find_element(By.ID, 'developers_list').text
        company = dc.cleanCompany(company)
    except:
        failed_log(True, '페이지 오픈 에러(thum, company)', '페이지가 제대로 열리지 않아서 생긴 오류입니다.', 'pc')
    
    
    # 게임 상세 정보
    try:
        description = wd.driver.find_element(By.ID, 'game_area_description').text
    except NoSuchElementException:
        description = 'description parsing failed :('
        
        failed_log(True,title,'description parsing failed','pc')
        
        
        
    # 스크린샷
    # 스크린샷 현재 흐린 이미지로 가져와서 고화질 원본 가져오는 작업 해야함
    #screenshot = driver.find_elements(By.CLASS_NAME, 'highlight_strip_item.highlight_strip_screenshot')
    #for scr in screenshot:
    #    screenList.append(scr.find_element(By.TAG_NAME, 'img').get_attribute('src'))
    
    
    screenshot = wd.driver.find_elements(By.CLASS_NAME, 'highlight_screenshot_link')
    
    for scr in screenshot:
        screenList.append(scr.get_attribute('href'))
    
    
    
    # 영문 이름
    engTitle = wd.driver_eng.find_element(By.ID, 'appHubAppName').text
    
    autokwd.append(dc.cleanKeyword(engTitle))
    autokwd.append(dc.cleanKeyword(title))
    
    autokwd = sorted(set(autokwd), key=lambda x: autokwd.index(x))
    
    detail_dict = {
        'imageurl': thum,
        'description': description,
        'autokwd': ",".join(autokwd),
        'company': company,
        'screenshot': ",".join(screenList),
        'tag':",".join(tagList),
        'platform': "steam"
    }
    
    #print(detail_dict)

    
    return detail_dict
    
    