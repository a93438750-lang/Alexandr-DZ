from selenium.webdriver.common.by import By
from selenium import webdriver


class CartPage:
    """
    Класс для работы со страницей корзины.
    """

    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver: webdriver.Chrome):
        """
        :param driver: Экземпляр WebDriver.
        """
        self.driver = driver

    def click_checkout(self):
        """
        Кликает по кнопке перехода к оформлению заказа.

        :return: None
        """
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()
