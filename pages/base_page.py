from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple

class BasePage:
    """
    Базовый класс для всех страниц. Содержит общие методы для взаимодействия с элементами.
    """
    def __init__(self, driver: webdriver.Chrome):
        """
        Инициализация базового класса страницы.

        :param driver: Экземпляр WebDriver для управления браузером.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator: Tuple[By, str]):
        """
        Находит элемент на странице с ожиданием его появления.

        :param locator: Локатор элемента в формате (By, value).
        :return: Найденный WebElement.
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def click_element(self, locator: Tuple[By, str]):
        """
        Находит элемент и кликает по нему.

        :param locator: Локатор элемента в формате (By, value).
        """
        element = self.find_element(locator)
        element.click()

    def input_text(self, locator: Tuple[By, str], text: str):
        """
        Находит элемент, очищает его и вводит текст.

        :param locator: Локатор элемента в формате (By, value).
        :param text: Строка текста для ввода.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)