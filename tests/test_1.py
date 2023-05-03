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
    """
    Добавляем в корзину случайное количество смартфонов в случайном порядке
    :return:
    Сравниваем список добавленных со списком находящихся в корзине
    """
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
        print(f'Добавили товар: {products[item][0]}', {products[item][1]})
    #product_page.wait_until_all_item_loaded()
    
    # список без кнопки в кортеже
    item_list = set()
    for item in products[:items_count_to_cart]:
        item_list.add(item[0])
    
    print('Переходим в корзину..')
    product_page.go_to_cart()
    assert product_page.get_current_url() == 'https://www.mvideo.ru/cart'
    print('OK')
    cart = Cart_page(driver)
    print('Определяем товары в корзине..')
    product_in_cart = set(cart.get_cart_item())
    # проверяем является ли множество добавленных товаров подмножеством товаров в корзине
    assert item_list.issubset(product_in_cart), 'Не все добавленные товары есть в корзине'
    print('OK.. Все добавленные товары есть в корзине')
    