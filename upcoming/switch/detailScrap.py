from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
import time
import re

from core.logs.failedLog import failed_log
from core.data_cleaning.DataCleaning import DataCleaning
from core.database.Database import Database

# 스위치 영문이름 데이터 통합 해결 방안
# 게임 데이터를 DB에 Autokwd 기준으로 검색
# 데이터가 검색이 되면 DB에 있는 영문이름을 스위치 name 변수에 덮어 씌우기
# 그러면 이름이 통합된다!

    

def extract_title(raw_title):
    raw_title = raw_title.replace('（','(').replace('）',')')
    eng_title = ''
    kor_title = ''
    match = re.search(r'\((.*?)\)', raw_title)
    
    if match:
        extracted_text = match.group(1)
        # 추출한 문자열이 영어인지 한국어인지 판별
        if all(ord(c) < 128 for c in extracted_text):
            eng_title = extracted_text.strip()
            kor_title = re.sub(r'\([^()]*\)', '', raw_title)
            return eng_title, kor_title
        else:
            kor_title = extracted_text.strip()
            eng_title = re.sub(r'\([^()]*\)', '', raw_title)
            return eng_title, kor_title
    else:
        eng_title = raw_title
        kor_title = raw_title
        
        return eng_title, kor_title

def get_description(driver):
    rawTextList = []
    description = None
    descRaw = driver.find_element(By.CLASS_NAME, 'product-attribute-content.expanded').find_elements(By.TAG_NAME,'p')
    
    
    if descRaw != []:
        for raw in descRaw:
            rawTextList.append(raw.text)
            description = "\n\n".join(rawTextList)
        
        return description
    else:
        description = driver.find_element(By.CLASS_NAME, 'product-attribute-content.expanded').text
        return description
    

def get_image(driver):
    # 홈페이지 리뉴얼로 인한 로직 변경
    # 스크린화면 클릭
    # 스크린샷 리스트 나오면 갯수 구하고
    # 이미지 수집 후 다음 버튼 클릭
    imgList = []
    
    
    driver.find_element(By.CLASS_NAME,'fotorama__img').click()
    
    
    imgNumber = driver.find_elements(By.CLASS_NAME, 'fotorama__nav__frame.fotorama__nav__frame--thumb')
    print(len(imgNumber))
    
        
    if len(imgNumber) == 0:
        img = driver.find_element(By.CLASS_NAME, 'fotorama__img--full').get_attribute('src')
        imgList.append(img)
        return imgList
        
    nextBtn = driver.find_element(By.CLASS_NAME, 'fotorama__arr.fotorama__arr--next')
    action = ActionChains(driver)
    for _ in range(len(imgNumber)):
        img = driver.find_element(By.CLASS_NAME, 'fotorama__img--full').get_attribute('src')
        imgList.append(img)
        action.move_to_element(nextBtn).perform()
        nextBtn.click()
        time.sleep(2)
    
    return imgList
    

def get_tag(driver):
    
    tagRaw = driver.find_element(By.CLASS_NAME,'product-attribute.game_category').find_element(By.CLASS_NAME, 'product-attribute-val').text
    
    print(tagRaw)
    try:
        tagRaw = tagRaw.replace(' ','')
        tagList = tagRaw.split(',')
        
    except:
        tagList.append(tagRaw)
        
    return tagList

def detail_scrap(driver, driver_eng, url, url_eng):
    # 스위치의 상세 정보 페이지의 첫 스크린샷 이미지는 썸네일
    
    db = Database()
    
    dc = DataCleaning('switch')
    
    autokwd = list()
    
    driver.implicitly_wait(60)
    
    driver.get(url)
    
    title = driver.find_element(By.CLASS_NAME, 'page-title').find_element(By.TAG_NAME,'span').find_element(By.TAG_NAME,'span').text
    
    filter_title = dc.cleanKeyword(title)
    print(filter_title)
    search_title = db.findGame(filter_title)
    
    print(search_title)
    
    eng_title, kor_title = extract_title(title)
    
    if search_title != None:
        autokwd.append(search_title)
        
    autokwd.append(dc.cleanKeyword(eng_title))
    autokwd.append(dc.cleanKeyword(kor_title))
    
    autokwd = sorted(set(autokwd), key= lambda x: autokwd.index(x))
    
    
    releaseDate = driver.find_element(By.CLASS_NAME, 'product-attribute.release_date').find_element(By.CLASS_NAME, 'product-attribute-val').text
    print(releaseDate)
    description = get_description(driver)
    tagList = get_tag(driver)
    company = driver.find_element(By.CLASS_NAME,'product-attribute.publisher').find_element(By.CLASS_NAME, 'product-attribute-val').text
    screenList = get_image(driver)
    
    thum = screenList[0]
    
    
    
    
    detail_dict = {
        'date': dc.formatDate(releaseDate),
        'imageurl': thum,
        'description': description,
        'autokwd': ",".join(autokwd),
        'company': company,
        'screenshot': ",".join(screenList),
        'tag':",".join(tagList),
        'platform': "switch"
    }
    
    print(detail_dict)
    return detail_dict