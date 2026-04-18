from selenium.webdriver.common.by import By
from selenium import webdriver


class CheckoutPage:
    """
    Класс для работы со страницей оформления заказа.
    """

    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    TOTAL_PRICE = (By.CLASS_NAME, "summary_total_label")

    def __init__(self, driver: webdriver.WebDriver):
        """
        :param driver: Экземпляр WebDriver.
        """
        self.driver = driver

    def fill_checkout_form(self, first_name: str, last_name: str, postal_code: str):
        """
        Заполняет форму оформления заказа данными пользователя.

        :param first_name: Имя пользователя (str).
        :param last_name: Фамилия пользователя (str).
        :param postal_code: Почтовый индекс (str).
        :return: None
        """
        (self.driver.find_element(*self.FIRST_NAME_FIELD).send_keys(first_name))
        (self.driver.find_element(*self.LAST_NAME_FIELD).send_keys(last_name))
        (self.driver.find_element(*self.POSTAL_CODE_FIELD).send_keys(postal_code))
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    def get_total_price(self) -> float:
        """
        Получает итоговую стоимость заказа со страницы и преобразует её в число.

        :return: Итоговая цена заказа (float).
                 Возвращает 0.0, если цена не найдена или не может быть преобразована.
        """
        try:
            total_text = self.driver.find_element(*self.TOTAL_PRICE).text
            # Убираем знак $ и пробелы,
            # оставляем только число
            price_str = total_text.replace("$", "").strip()
            return float(price_str)
        except Exception:
            return 0.0
