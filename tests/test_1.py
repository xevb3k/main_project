import time
from pages.login_page import Login_page
from pages.product_page import Product_page
from pages.cart_page import Cart_page
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import random

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
#driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

def test_add_products_to_cart():
    random.seed()
    login_page = Login_page(driver)
    login_page.location_window_close()
    print('Раскрываем каталог..')
    ActionChains(driver).move_to_element(login_page.button_catalog).perform()
    ActionChains(driver).click().perform()
    print('Выбираем смартфоны..')
    ActionChains(driver).move_to_element(login_page.catalog_smf_gadget).perform()
    ActionChains(driver).move_to_element(login_page.product_cmf).perform()
    ActionChains(driver).click().perform()
    product_page = Product_page(driver)
    
    print('Актвируем фильтр по бренду..')
    product_page.select_brand(['Apple', 'Honor', 'Samsung'])
    time.sleep(1)
    
    product_page.switch_list_grid()
    time.sleep(1)
    
    # список товаров
    products = product_page.get_products()
    print('Активных карт товара:', len(products))
    # добавляем случайное число товаров в корзину в случайном порядке
    items_count_to_cart = random.randint(1, len(products)-1)
    print(f'Будем добавлять в корзину: {items_count_to_cart} товаров')
    random.shuffle(products)
    for item in range(items_count_to_cart):
        product_page.put_to_cart(products[item][2], True)
        print(f'Добавили товар: {products[item][0]}')
    #product_page.wait_until_all_item_loaded()
    
    # список без кнопки в кортеже
    item_list = []
    for item in products[:items_count_to_cart]:
        item_list.append((item[0], item[1]))
    
    print('Переходим в корзину..')
    product_page.go_to_cart()
    assert product_page.get_current_url() == 'https://www.mvideo.ru/cart'
    print('OK')
    cart = Cart_page(driver)
    print('Определяем товары в корзине..')
    product_in_cart = cart.get_cart_item()
    assert len(product_in_cart) == len(item_list), '! Неверное количество товаров в корзине'
    assert product_in_cart.sort() == item_list.sort(), '! Неверные товары в корзине'
    print('OK')
    