import allure
import pytest

from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from helpers.helpers_on_check_response import check_status_code, check_success, check_key_in_body, _print_info, \
    check_ingredients_list
from helpers.helpers_on_get_ingredients import try_to_get_ingredients, get_buns_list, get_fillings_list, get_sauces_list
from helpers.helpers_on_requests import request_on_get_ingredients


# Получаем данные об ингредиентах от API
@allure.title('Получаем данные об ингредиентах')
@pytest.fixture(scope="session")
def get_ingredients_from_api():
    return check_ingredients_list(try_to_get_ingredients())


@allure.title('Получаем список булок')
@pytest.fixture(scope="session")
def get_buns_list_from_api(get_ingredients_from_api):
    return get_buns_list(get_ingredients_from_api)


@allure.title('Получаем список начинок')
@pytest.fixture(scope="session")
def get_fillings_list_from_api(get_ingredients_from_api):
    return get_fillings_list(get_ingredients_from_api)


@allure.title('Получаем список соусов')
@pytest.fixture(scope="session")
def get_sauces_list_from_api(get_ingredients_from_api):
    return get_sauces_list(get_ingredients_from_api)



