from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

class Base_page:
    
    def __init__(self, driver):
        self.driver = driver

    def get_current_url(self):
        return self.driver.current_url
