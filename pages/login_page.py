import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys
from base.base_page import Base_page
import allure

default_timeout = 5
elements = {'button_catalog': [(By.XPATH, "//*[text()='Каталог']"), default_timeout],
            'catalog_smf_gadget': [(By.XPATH, "//*[text()='Смартфоны и гаджеты']"), default_timeout],
            'product_cmf': [(By.XPATH, "//*[text()='Смартфоны']"), default_timeout]
            }

locator_location_window= (By.XPATH, "//div[@class='location-interactive']")

url = 'https://www.mvideo.ru/'


class Login_page(Base_page):

    def __init__(self, driver):
        super().__init__(driver)
        self.url = url
        self.driver.get(self.url)
        #self.driver.maximize_window()
        
    def __getattribute__(self, item):
        # метод ищет элекмент на странице, если он есть в словаре elements
        elem = elements.get(item)
        if elem:
            return WebDriverWait(self.driver, elem[1]).until(EC.element_to_be_clickable(elem[0]))
        return super().__getattribute__(item)
    
    def location_window_close(self):
        """
        Удаляет всплывающее окно локации
        :return:
        """
        with allure.step('Закрыть окно локации'):
            location_window = self.driver.find_elements(*locator_location_window)
            if len(location_window) != 0:
                self.driver.execute_script("arguments[0].remove();", location_window[0])
            
