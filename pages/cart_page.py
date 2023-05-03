import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys
from base.base_page import Base_page
from selenium.webdriver.common.action_chains import ActionChains
import allure

default_timeout = 5

# locator_cart_prod_container = (By.XPATH, "//div[@class='cart-item']")
# locator_cart_prod_container_kit = (By.XPATH, "//div[@class='cart-promo-kit']")
# locator_cart_item = (By.XPATH, "//li[@class='cart-items__item ng-star-inserted']")
# locator_cart_item_from_kit = (By.XPATH, "//li[@class='cart-promo-kit__item ng-star-inserted']")
# locator_cart_item_price = (By.XPATH, ".//span[@class='price__main-value']")

locator_cart_item_name = (By.XPATH, ".//div[@class='cart-item__name-container']/h3/a")

class Cart_page(Base_page):
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_cart_item(self):
        """
        Возвращает список товаров в корзине
        :return:
        список кортежей (товар, цена)
        """
        with allure.step('Получаем товары из корзины'):
            cart_prod_items = WebDriverWait(self.driver, default_timeout).until(EC.presence_of_all_elements_located(locator_cart_item_name))
            count_item_in_cart = len(cart_prod_items)
            print(f'Товаров в корзине: {count_item_in_cart}')
            
            cart_list = []
            actions = ActionChains(self.driver)
            for item in cart_prod_items:
                actions.move_to_element(item).perform()
                print('Присутствует в корзине: ', item.text)
                cart_list.append(item.text)
                
            return cart_list
        
        
        