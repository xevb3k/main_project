import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys
from base.base_page import Base_page

default_timeout = 5


locator_cart_prod_container = (By.XPATH, "//div[@class='cart-item']")

locator_cart_item = (By.XPATH, "//li[@class='cart-items__item ng-star-inserted']")
locator_cart_item_name = (By.XPATH, ".//div[@class='cart-item__name-container']/h3/a")
locator_cart_item_price = (By.XPATH, ".//span[@class='price__main-value']")

class Cart_page(Base_page):
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_cart_item(self):
        """
        Возвращает список товаров в корзине
        :return:
        список кортежей (товар, цена)
        """
        cart_prod_items = WebDriverWait(self.driver, default_timeout).until(EC.presence_of_all_elements_located(locator_cart_item))
        count_item_in_cart = len(cart_prod_items)
        print(f'Товаров в корзине: {count_item_in_cart}')
        
        cart_list = []
        for item in cart_prod_items:
            item_name = WebDriverWait(item, default_timeout).until(EC.presence_of_element_located(locator_cart_item_name))
            item_price = WebDriverWait(item, default_timeout).until(EC.presence_of_element_located(locator_cart_item_price))
            print(item_name.text, item_price.text)
            cart_list.append((item_name.text, item_price.text))
            
        return cart_list
        
        
        