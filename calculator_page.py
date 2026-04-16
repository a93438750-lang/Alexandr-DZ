from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

class CalculatorPage:
    """
    Класс для работы с калькулятором на сайте bonigarcia.
    """
    def __init__(self, driver):
        self.driver = driver
        self.URL = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"

    # Локаторы
    OPERANDS = (By.CSS_SELECTOR, "input[name^='operand']") # Найдет все 4 поля
    OPERATION = (By.NAME, "operation")
    EQUALS_BUTTON = (By.NAME, "calculate")
    RESULT = (By.ID, "result")
    DELAY = (By.NAME, "delay")

    def open(self):
        """Открывает страницу калькулятора."""
        self.driver.get(self.URL)
        # Ждем, пока кнопка "Calculate" станет кликабельной
        time.sleep(2) 
    
    def click_button_7(self):
        """Вводит цифру 7 в первое доступное поле операнда."""
        fields = self.driver.find_elements(*self.OPERANDS)
        if fields:
            fields[0].send_keys("7")

    def click_button_8(self):
        """Вводит цифру 8 во второе доступное поле операнда."""
        fields = self.driver.find_elements(*self.OPERANDS)
        if len(fields) > 1:
            fields[1].send_keys("8")

    def click_plus(self):
        """Выбирает операцию сложения (+)."""
        select = Select(self.driver.find_element(*self.OPERATION))
        select.select_by_visible_text("+")
        
    def click_equals(self):
        """Кликает по кнопке вычисления (=)."""
        self.driver.find_element(*self.EQUALS_BUTTON).click()
        
    def get_result(self):
        """Получает текст из поля результата."""
        try:
            return self.driver.find_element(*self.RESULT).get_attribute("value")
        except:
            return ""

    def set_delay(self, value: str):
        """Устанавливает значение задержки."""
        try:
            delay_field = self.driver.find_element(*self.DELAY)
            delay_field.clear()
            delay_field.send_keys(value)
        except:
            pass