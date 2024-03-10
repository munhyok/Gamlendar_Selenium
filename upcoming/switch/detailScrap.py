from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re

from core.logs.failedLog import failed_log
from core.data_cleaning.DataCleaning import DataCleaning

def extract_title(raw_title):
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
    try:
        descRaw = driver.find_element(By.CLASS_NAME, 'product.attribute.mfr_description').find_element(By.CLASS_NAME, 'value').find_elements(By.TAG_NAME,'p')
        for rawText in descRaw:
            rawTextList.append(rawText.text)
            description = "\n".join(rawTextList)
        
    except NoSuchElementException:
        description = driver.find_element(By.CLASS_NAME, 'product.attribute.mfr_description').find_element(By.CLASS_NAME, 'value').text

    return description

def get_image(driver):
    # 아.. before-active-after 슬라이더 구조 넘어갈때마다 이벤트 발생
    # dot length 구하고 length - 1 next 클릭
    # active 된 이미지만 href 링크 받아오기 (aria-hidden = false -> acitve image)
    imgList = []
    
    dotNumber = driver.find_element(By.CLASS_NAME,'fotorama__nav__shaft').find_elements(By.CLASS_NAME,'fotorama__nav__frame.fotorama__nav__frame--dot')
    nextBtn = driver.find_element(By.CLASS_NAME,'fotorama__arr.fotorama__arr--next')
    

    for _ in range(len(dotNumber)):
        imgs = driver.find_element(By.CLASS_NAME,'fotorama__stage__shaft.fotorama__grab').find_elements(By.TAG_NAME, 'div')
        
        
        for img in imgs:
            if img.get_attribute('aria-hidden') == 'false':
                imgList.append(img.get_attribute('href'))
                
                
        time.sleep(2)
        nextBtn.click()
        
    #print(imgList)
    return imgList

def get_tag(driver):
    
    tagRaw = driver.find_element(By.CLASS_NAME,'product-attribute.game_category').find_element(By.CLASS_NAME, 'product-attribute-val').text
    
    try:
        tagRaw = tagRaw.replace(' ','')
        tagList = tagRaw.split(',')
        
    except:
        tagList.append(tagRaw)
        
    return tagList

def detail_scrap(driver, driver_eng, url, url_eng):
    # 스위치의 상세 정보 페이지의 첫 스크린샷 이미지는 썸네일
    
    dc = DataCleaning('switch')
    
    autokwd = list()

    driver.implicitly_wait(60)
    
    driver.get(url)
    
    wait = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, "fotorama__nav__shaft")))
    
    title = driver.find_element(By.CLASS_NAME, 'page-title').find_element(By.TAG_NAME,'span').text
    
    eng_title, kor_title = extract_title(title)
    
    autokwd.append(eng_title)
    autokwd.append(kor_title)
    
    autokwd = sorted(set(autokwd), key= lambda x: autokwd.index(x))
    
    releaseDate = driver.find_element(By.CLASS_NAME, 'product-attribute.release_date').find_element(By.CLASS_NAME, 'product-attribute-val').text
    description = get_description(driver)
    company = driver.find_element(By.CLASS_NAME,'product-page-pusblisher-attr').text
    screenList = get_image(driver)
    
    thum = screenList[0]
    tagList = get_tag(driver)
    
    
    
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