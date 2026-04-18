from selenium.webdriver.common.by import By
from selenium import webdriver


class LoginPage:
    """
    Класс для работы со страницей авторизации.
    """

    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def __init__(self, driver: webdriver.Chrome):
        """
        :param driver: Экземпляр WebDriver.
        """
        self.driver = driver

    def enter_username(self, username: str):
        """
        Вводит имя пользователя в соответствующее поле.

        :param username: Имя пользователя (str).
        :return: None
        """
        self.driver.find_element(*self.USERNAME_FIELD).send_keys(username)

    def enter_password(self, password: str):
        """
        Вводит пароль в соответствующее поле.

        :param password: Пароль пользователя (str).
        :return: None
        """
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def click_login(self):
        """
        Кликает по кнопке входа в систему.

        :return: None
        """
        self.driver.find_element(*self.LOGIN_BUTTON).click()
