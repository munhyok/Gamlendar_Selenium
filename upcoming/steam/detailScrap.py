from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# 수집 목록
# Thum, description, company, tag, screenshot, english name
# 한국어, 영어 별도로 driver를 만들어서 2개 돌려야 수집 속도가 올라갈듯..



LOADING_PAGE = 2




def pass_adult(driver, driver_english):
    # 어차피 한 번만 인증하면 되기 때문에 GTA5에서 미리 인증을 거치고
    # 추후 게임 데이터 수집을 시작
    
    driver.get('https://store.steampowered.com/agecheck/app/271590/')
    driver_english.get('https://store.steampowered.com/agecheck/app/271590/')

    time.sleep(1)
    driver.find_element(By.ID, 'ageYear').click()
    driver_english.find_element(By.ID, 'ageYear').click()
    time.sleep(0.5)
    
    
    driver.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[6]/div/div[2]/div/div[1]/div[3]/select[3]/option[91]').click()
    driver_english.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[6]/div/div[2]/div/div[1]/div[3]/select[3]/option[91]').click()
    
    
    time.sleep(0.5)
    
    driver.find_element(By.ID, 'view_product_page_btn').click()
    driver_english.find_element(By.ID, 'view_product_page_btn').click()
    
    


def detail_scrap(driver, driver_english, url):
    
    
    
    autokwdSet = set()
    screenList = []
    tagList = []
    detailList = []
    
    driver.get(url)
    driver_english.get(url)

    
    time.sleep(3)
    
    
    tags = driver.find_element(By.CLASS_NAME, 'glance_tags.popular_tags').find_elements(By.CLASS_NAME,'app_tag')
    
    for tag in tags:
        plain = tag.text
        if not plain == '':
            tagList.append(plain)
    tagList.remove('+')
        
        
    # 이 태그가 들어간 친구들은 수집 금지
    adultTag = ['헨타이','후방주의','선정적인 내용']
    
    for adult in adultTag:
        if adult in tagList:
            print("adult game")
            return None
            
        
        
        
    title = driver.find_element(By.ID, 'appHubAppName').text
    thum = driver.find_element(By.CLASS_NAME, 'game_header_image_full').get_attribute('src')
    description = driver.find_element(By.ID, 'game_area_description').text
    company = driver.find_element(By.ID, 'developers_list').text
    screenshot = driver.find_elements(By.CLASS_NAME, 'highlight_strip_item.highlight_strip_screenshot')
    for scr in screenshot:
        screenList.append(scr.find_element(By.TAG_NAME, 'img').get_attribute('src'))
    
    autokwdSet.add(title)
    
    
    
    
    
    
    
    
    title_english = driver_english.find_element(By.ID, 'appHubAppName').text
    autokwdSet.add(title_english)
    
    autokwd = list(autokwdSet)
    
    detail_dict = {
        'imageurl': thum,
        'description': description,
        'autokwd': autokwd,
        'company': company,
        'screenshot': screenList,
        'tag':tagList,
        'platform': ["PC"]
    }
    
    print(detail_dict)
    
    #detailList.append(detail_dict)
    
    return detail_dict
    
    
# testMode
#driver = webdriver.Chrome()
#driver_english = webdriver.Chrome()

#detail_scrap(driver,driver_english, 'https://store.steampowered.com/agecheck/app/553850/')
#pass_adult(driver, driver_english)