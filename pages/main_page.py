from selenium.webdriver.common.by import By
from selenium import webdriver

class MainPage:
    """
    Класс для работы с главной страницей магазина.
    """
    BACKPACK_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    BOLT_TSHIRT_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    ONESIE_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-onesie")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver: webdriver.Chrome):
        """
        :param driver: Экземпляр WebDriver.
        """
        self.driver = driver

    def add_backpack_to_cart(self):
        """
        Добавляет рюкзак в корзину.

        :return: None
        """
        self.driver.find_element(*self.BACKPACK_ADD_BUTTON).click()

    def add_bolt_tshirt_to_cart(self):
        """
        Добавляет футболку Bolt в корзину.

        :return: None
        """
        self.driver.find_element(*self.BOLT_TSHIRT_ADD_BUTTON).click()

    def add_onesie_to_cart(self):
        """
        Добавляет комбинезон Onesie в корзину.

        :return: None
        """
        self.driver.find_element(*self.ONESIE_ADD_BUTTON).click()

    def go_to_cart(self):
        """
         Переходит на страницу корзины по иконке корзины.

         :return: None
         """
        self.driver.find_element(*self.CART_ICON).click()