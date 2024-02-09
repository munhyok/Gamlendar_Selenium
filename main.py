from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from upcoming.steam.steam_main import steam_upcoming
from upcoming.playstation.playstation_main import playstation_upcoming
from upcoming.xbox.xbox_main import xbox_upcoming
from upcoming.switch.switch_main import switch_upcoming

import time

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

steam_upcoming(driver, driver_eng)
playstation_upcoming(driver, driver_eng)
xbox_upcoming(driver, driver_eng)
switch_upcoming(driver, driver_eng)

driver.quit()
driver_eng.quit()