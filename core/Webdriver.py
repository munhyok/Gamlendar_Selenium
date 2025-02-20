import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Webdriver:
    
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Webdriver, cls).__new__(cls)
        
        return cls._instance
    
    def __init__ (self):
        userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"

        self.options = Options()
        self.options.add_argument("user-agent="+userAgent)
        self.options.add_argument("lang=ko_KR")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--headless=new')

        
        
    def startDriver(self):
        
        # ---Execute Selenium---
        
        self.driver = webdriver.Chrome(options=self.options)
        self.driver_eng = webdriver.Chrome(options=self.options)
    
    def restartDriver(self):
        try:
            self.quitDriver()
        except Exception as e:
            print(f"Error during driver quit: {e}")
            
        print('5분 뒤에 다시 시작')
        
        time.sleep(300)
        newUserAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
        #
        #PROXY = '43.200.77.128:3128'
        #webdriver.DesiredCapabilities.CHROME['proxy'] = {
        #    "httpProxy": PROXY,
        #    "ftpProxy": PROXY,
        #    "sslProxy": PROXY,
        #    "proxyType": "MANUAL"
        #}
        
        
        self.options = Options()
        self.options.add_argument("user-agent="+newUserAgent)
        self.options.add_argument("lang=ko_KR")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.startDriver()

    def refreshPage(self):
        print("페이지 수집 오류 5분뒤에 페이지 새로고침 후 재시도")
        time.sleep(300)
        self.driver.refresh()
        self.driver_eng.refresh()
        
        
    def quitDriver(self):
        self.driver.quit()
        self.driver_eng.quit()