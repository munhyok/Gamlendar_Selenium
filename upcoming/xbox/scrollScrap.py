from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


FILTERWORDS = ['디럭스', 'Deluxe', '프리미엄', 'Premium', '얼티밋', 'Ultimate', '컴플리트', 'Complete', '디피니티브', 'Definitive']

def scroll_scrap(driver):
    
    wait = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='gameDivLink']")))
    print('Loading Done, Scrap start')
    
    #driver.find_element(By.CSS_SELECTOR, )
    
    