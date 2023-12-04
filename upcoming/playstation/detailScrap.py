from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

LOADING_PAGE = 2



def detail_scrap(driver, driver_eng, url, url_eng):
    
    driver.get(url)
    driver_eng.get(url_eng)
    
    
    thum = driver.find_element(By.XPATH, '/html/body/div[3]/main/div/div[1]/div[1]/div/div/div/div/span/img[2]').get_attribute('src')
    description = driver.find_element(By.CSS_SELECTOR, "div[class='psw-l-w-1/1 psw-l-w-2/3@tablet-s psw-l-w-2/3@tablet-l psw-l-w-1/2@laptop psw-l-w-1/2@desktop psw-l-w-1/2@max']").find_element(By.TAG_NAME, 'p').text
    company = driver.find_element(By.CSS_SELECTOR, "dd[data-qa='gameInfo#releaseInformation#publisher-value']").text
    
    releaseDate = driver.find_element(By.CSS_SELECTOR, "dd[data-qa='gameInfo#releaseInformation#releaseDate-value']").text
    
    
    
    title = driver.find_element(By.CSS_SELECTOR, "h1[data-qa='mfe-game-title#name']").text
    
    #한국 페이지에는 있지만 해외 페이지에는 없을 때
    try:
        engTitle = driver_eng.find_element(By.CSS_SELECTOR, "h1[data-qa='mfe-game-title#name']").text
    except NoSuchElementException:
        engTitle = None
        
        
        
        
        
    print(thum)
    print(company)
    print(description)
    print(releaseDate)
    print('-'*20)
    print(title)
    print(engTitle)
    
    