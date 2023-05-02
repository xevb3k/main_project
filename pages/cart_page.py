import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys
from base.base_page import Base_page

default_timeout = 5
locator_products_name = (By.XPATH, "//a[@class='cart-item__name ng-star-inserted']")
locator_products_price = (By.XPATH, "//span[@class='price__main-value']")
locator_cart_prod_container = (By.XPATH, "//div[@class='cart-item']")

locator_cart_item = (By.XPATH, "//li[@class='cart-items__item ng-star-inserted']")

class Cart_page(Base_page):
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_cart_item(self):
        cart_prod_items = WebDriverWait(self.driver, default_timeout).until(EC.presence_of_all_elements_located(locator_cart_item))
        print(len(cart_prod_items))
        return len(cart_prod_items)
        
        
        