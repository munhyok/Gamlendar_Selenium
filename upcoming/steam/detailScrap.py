from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# 수집 목록
# Thum, description, company, tag, screenshot, english name


#driver = webdriver.Chrome()
LOADING_PAGE = 2

def pass_adult(driver):
    
    pass


def detail_scrap(driver, url):
    
    autokwdSet = set()
    screenList = []
    tagList = []
    detailList = []
    
    driver.get(url)
    #time.sleep(5)
    driver.execute_script('ChangeLanguage("koreana")')
    
    time.sleep(5)
    
    
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
    
    
    driver.execute_script('ChangeLanguage("english")')
    
    
    time.sleep(5)
    
    
    title = driver.find_element(By.ID, 'appHubAppName').text
    autokwdSet.add(title)
    
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
    
#detail_scrap(driver, 'https://store.steampowered.com/app/1061280/Plastic_Love/?snr=1_7_7_popularwishlist_150_12') #testMode