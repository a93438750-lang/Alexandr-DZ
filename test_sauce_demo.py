import pytest
import allure
from selenium import webdriver
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()

@allure.feature("Функциональность магазина (Sauce Demo)")
class TestSauceDemoFunctionality:

    @allure.title("Успешная покупка трех товаров")
    @allure.description("Тест проверяет полный цикл покупки: авторизация, добавление товаров в корзину, оформление заказа и проверка итоговой суммы.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_shop_functionality(self, driver):
        
        BASE_URL = "https://www.saucedemo.com/"
        USERNAME = "standard_user"
        PASSWORD = "secret_sauce"
        FIRST_NAME = "Test"
        LAST_NAME = "User"
        POSTAL_CODE = "12345"
        EXPECTED_TOTAL = 29.98 # Сумма цен трех товаров: 29.98

        with allure.step("Открытие страницы логина"):
            driver.get(BASE_URL)

        # Авторизация
        with allure.step("Авторизация пользователя"):
            login_page = LoginPage(driver)
            login_page.enter_username(USERNAME)
            login_page.enter_password(PASSWORD)
            login_page.click_login()

        # Добавление товаров в корзину
        with allure.step("Добавление товаров в корзину"):
            main_page = MainPage(driver)
            main_page.add_backpack_to_cart()
            main_page.add_bolt_tshirt_to_cart()
            main_page.add_onesie_to_cart()

        # Переход в корзину и оформление
        with allure.step("Переход в корзину и оформление заказа"):
            main_page.go_to_cart()
            
            cart_page = CartPage(driver)
            cart_page.click_checkout()

            checkout_page = CheckoutPage(driver)
            checkout_page.fill_checkout_form(FIRST_NAME, LAST_NAME, POSTAL_CODE)
        
        # Проверка итоговой суммы (вынесем в отдельный шаг для наглядности)
        with allure.step("Получение итоговой суммы заказа"):
            total_price = checkout_page.get_total_price()
        
        # Проверка (Assertion)
        with allure.step("Проверка, что итоговая сумма совпадает с ожидаемой"):
            assert total_price == EXPECTED_TOTAL, f"Ожидаемая сумма {EXPECTED_TOTAL}, но получена {total_price}"