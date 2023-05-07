import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys
from base.base_page import Base_page
from selenium.webdriver.common.action_chains import ActionChains
import allure

default_timeout = 5

locator_filter_container = (By.XPATH, "//mvid-filter-checkbox-list")
locator_filter_showall = (By.XPATH, "//p[text()=' Показать ещё ']")
locator_in_cart_buttons = (By.XPATH, "//mvid-button[@class='cart-button button_without-icon']")
locator_products_name = (By.XPATH, "//a[@class='product-title__text']")
locator_products_price = (By.XPATH, "//span[@class='price__main-value']")
locator_cart = (By.XPATH, "//p[text()='Корзина']")

locator_list_product_card = (By.XPATH, "//div[contains(@class, 'product-cards-layout__item')]")
locator_product_card_name = (By.XPATH, ".//a[contains(@class, 'product-title__text')]")
locator_product_card_price = (By.XPATH, ".//span[contains(@class, 'price__main-value')]")
#locator_product_not_available = (By.XPATH, ".//div[contains(@class, 'product-notification') and contains(text(), 'Нет в наличии')]")
locator_list_lazy_load = (By.XPATH, '//mvid-lazy-render')
locator_filter_available_only = (By.XPATH, "//span[contains(@class, 'filter-name') and text()=' Только в наличии ']")
locator_product_in_cart_button_old = (By.XPATH, ".//button[contains(@class, 'button') and @title='Добавить в корзину']")
locator_product_in_cart_button = (By.XPATH, ".//mvid-button[contains(@class, 'cart-button')]")
locator_product_in_cart_buttons_loading = (By.XPATH, ".//button[contains(@class, 'button--loading')]")
locator_product_in_cart_all_buttons_loading = (By.XPATH, "//button[contains(@class, 'button--loading')]")

locator_cookies_close_button = (By.XPATH, "//div[@class='mv-main-button--content' and contains(text(),'Понятно')]")
locator_cart_popup_window = (By.XPATH, "//div[contains(@class, 'tooltip__item')]")
locator_product_grid_switch = (By.XPATH, "//div[contains(@class, 'listing-view-switcher__pointer--grid')]")
locator_product_grid_switch_button = (By.XPATH, "//mvid-button[contains(@class, 'listing-view-switcher__button')]/button")

class Product_page(Base_page):
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def select_brand(self, brand_name_list):
        """
        Фильтрует товары по бренду
        :param brand_name_list: список брендов
        :return:
        """
        with allure.step(f'Выбор брендов {brand_name_list}'):
            # контейнер со всеми фильтрами для смартфонов
            filter_container = WebDriverWait(self.driver, default_timeout).until(EC.presence_of_all_elements_located(locator_filter_container))
            # второй фильтр - контейнер с брендами
            filter_brand_container = filter_container[1]
            # покажем весь список брендов
            filter_brand_showall = WebDriverWait(filter_brand_container, default_timeout).until(EC.presence_of_element_located(locator_filter_showall))
            filter_brand_showall.click()
            # внутри контейнера с брендами ищем бренд по списку и кликаем его
            for brand_name in brand_name_list:
                locator_filter_brand = (By.XPATH, f'.//a[text()=" {brand_name} "]')
                print(f' {brand_name}.. OK')
                filter_brand = WebDriverWait(filter_brand_container, default_timeout).until(EC.presence_of_element_located(locator_filter_brand))
                filter_brand.click()
                time.sleep(2)

    def cookie_notification_close(self):
        """
        Закрывает уведомление о куках
        :return:
        """
        with allure.step('Закрыть окно уведомления о куках'):
            cookies_close_button = self.driver.find_elements(*locator_cookies_close_button)
            if len(cookies_close_button) != 0:
                cookies_close_button[0].click()
            
    def switch_list_grid(self):
        """
        Переключает сетку товаров на список, если еще не список
        :return:
        """
        with allure.step('Переключить отображение товаров с сетки на список'):
            switch_indicator = self.driver.find_elements(*locator_product_grid_switch)
            if len(switch_indicator) != 0:
                print('Переключение сетки товаров на список..')
                switch_button = WebDriverWait(self.driver, default_timeout).until(EC.presence_of_element_located(locator_product_grid_switch_button))
                switch_button.click()
            print('Товары отображены списком')
            
    def cart_popup_window_close(self):
        """
        Удаляет всплывающее окно корзины
        :return:
        """
        with allure.step('Убрать всплывающее окно корзины'):
            cart_popup_window = self.driver.find_elements(*locator_cart_popup_window)
            if len(cart_popup_window) != 0:
                self.driver.execute_script("arguments[0].remove();", cart_popup_window[0])
            
    def put_to_cart(self, item, wait_for_loading=False):
        """
        Добавляет товар в корзину
        :param item: кнопка "Добавить в корзину" (WebElement)
        wait_for_loading: ждать загрузки элемента в корзину
        :return:
        """
        with allure.step('Добавление товара в корзину'):
            actions = ActionChains(self.driver)
            actions.move_to_element(item).perform()
            self.cart_popup_window_close()
            window_y = self.driver.execute_script("return window.pageYOffset;")
            # если кнопка попала под хедер сайта
            loc_y = item.location.get('y')
            if loc_y-window_y <= 113:
                print('Допскролл..')
                #print(f'window_y={window_y}, y={loc_y}')
                self.driver.execute_script("window.scrollBy(0, -200);") # ширина футера 113, с запасом 217
            item.click()
            if wait_for_loading:
                WebDriverWait(item, default_timeout).until(EC.invisibility_of_element_located(locator_product_in_cart_buttons_loading))

    def wait_until_all_item_loaded(self):
        """
        Ждет когда все элементы попадут в корзину (индикаторы загрузки на кнопках пропадут)
        :return:
        """
        with allure.step('Ожидание пока все товары добавяется'):
            WebDriverWait(self.driver, default_timeout).until(EC.invisibility_of_element_located(locator_product_in_cart_all_buttons_loading))

    def get_products(self):
        """
        Возвращает список товаров со страницы
        :return: список кортежей в формате (имя_товара, цена, WebElement кнопка_добавления_в_корзину)
        """
        with allure.step('Получение списка товаров'):
            actions = ActionChains(self.driver)
            # все карточки товаров на странице
            products_cards = WebDriverWait(self.driver, default_timeout).until(EC.presence_of_all_elements_located(locator_list_product_card))
            print('Найдено карт товаров на странице ', len(products_cards))
            
            # 1 способ обойти lazyload - крутить вниз по 200пикс
            # while len(self.driver.find_elements(*locator_list_lazy_load)) > 0:
            #     self.driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
            # создаем список продуктов
            product_list = []
            for product in products_cards:
                # 2й способ обойти lazyload - двигаемся к каждой из карт товара, что бы прогрузились тэги с description
                actions.move_to_element(product).perform()
                
                # извлекаем имя продукта
                product_name = WebDriverWait(product, default_timeout).until(EC.presence_of_element_located(locator_product_card_name))
                # если продукт есть в наличии
                product_available = product.find_elements(*locator_product_card_price)
                if product_available:
                    # извлекаем его цену и кнопку в корзину
                    product_price = WebDriverWait(product, default_timeout).until(EC.presence_of_element_located(locator_product_card_price)).text
                    product_button_in_cart = WebDriverWait(product, default_timeout).until(EC.element_to_be_clickable(locator_product_in_cart_button))
                    # если есть попап про куки - гасим
                    self.cookie_notification_close()
                    product_list.append((product_name.text, product_price, product_button_in_cart))
            return product_list
    
    def go_to_cart(self):
        """
        Переходим в корзину
        :return:
        """
        with allure.step('Переход в корзину'):
            cart = WebDriverWait(self.driver, default_timeout).until(EC.presence_of_element_located(locator_cart))
            cart.click()
        