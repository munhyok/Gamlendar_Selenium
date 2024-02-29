from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
#from core.logs.failedLog import failed_log
import time
from selenium.webdriver.chrome.options import Options



def find_bundle(driver, driver_eng):
    bundleList = []
    tmp_title = ''
    tmp_url = ''
    try:
        bundleList = driver.find_element(By.CSS_SELECTOR,"section[aria-label='이 번들']").find_element(By.CSS_SELECTOR, "div[class='ModuleRow-module__row___N1V3E']").find_element(By.CSS_SELECTOR, "ol[class='ItemsSlider-module__wrapper___nAi6y']").find_elements(By.TAG_NAME, 'li')

        bundleList.pop()
        print(bundleList)
        
        print(len(bundleList))
        for titles in bundleList:
            title = titles.find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME,'a').get_attribute('title')
            link = titles.find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME,'a').get_attribute('href')


            title = title.replace('Xbox Series X|S용 ','').replace('Xbox One용 ','').replace(' Xbox One', '').replace(' Xbox Series X|S','')

            print(title)
            if tmp_title == '':
                tmp_title = title
                tmp_url = link
                

            elif len(title) < len(tmp_title):
                
                tmp_title = title
                tmp_url = link
            
            print(tmp_title)
            
        print(tmp_title)
        print(tmp_url)
        driver.get(tmp_url)
        driver_eng.get(tmp_url.replace('ko-KR', 'en-us'))
        time.sleep(10)
        
        
        
    except NoSuchElementException:
        print("this is not bundle")
        
        return None
    
def main():
    userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"

    options = Options()
    options.add_argument("user-agent="+userAgent)
    options.add_argument("lang=ko_KR")
    options.add_argument("--disable-gpu")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    #options.add_argument('--headless=new')

    driver = webdriver.Chrome(options=options)
    driver_eng = webdriver.Chrome(options=options)
    
    driver.get("https://www.xbox.com/ko-kr/games/store/xbox-one-wwe-2k24--/9NZTJHFXX8RS")
    driver_eng.get("https://www.xbox.com/ko-kr/games/store/xbox-one-wwe-2k24--/9NZTJHFXX8RS")
    find_bundle(driver, driver_eng)
    
    
main()