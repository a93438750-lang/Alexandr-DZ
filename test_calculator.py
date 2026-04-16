import pytest
import allure
from selenium import webdriver
from calculator_page import CalculatorPage
import time

@allure.feature("Функциональность калькулятора")
class TestCalculator:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.calculator_page = CalculatorPage(self.driver)
        yield
        self.driver.quit()

    @allure.title("Проверка функции отложенного результата")
    @allure.description("Тест проверяет, что калькулятор правильно считает сумму после заданной задержки.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_calculator_functionality(self):
        
        with allure.step("Открытие страницы калькулятора"):
            self.calculator_page.open()
        
        with allure.step("Установка задержки выполнения на 45 секунд"):
            self.calculator_page.set_delay("45")
        
        with allure.step("Ввод выражения: 7 + 8"):
            self.calculator_page.click_button_7()
            self.calculator_page.click_plus()
            self.calculator_page.click_button_8()
            self.calculator_page.click_equals()
        
        with allure.step("Ожидание завершения вычисления (46 секунд)"):
            time.sleep(46)
        
        with allure.step("Получение результата с экрана"):
            result = self.calculator_page.get_result()
        
        with allure.step("Проверка результата вычисления"):
            assert result == "15", f"Ожидаемый результат: 15, фактический: {result}"