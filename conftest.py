import allure
import pytest

from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from helpers.helpers_on_check_response import check_status_code, check_success, check_key_in_body, _print_info, \
    check_ingredients_list
from helpers.helpers_on_get_ingredients import try_to_get_ingredients, get_buns_list, get_fillings_list, get_sauces_list
from helpers.helpers_on_requests import request_on_get_ingredients


#from helpers.helpers_on_create_user import try_to_get_ingredients


# Получаем данные об ингредиентах от API
@allure.title('Получаем данные об ингредиентах')
@pytest.fixture(name='get_ingredients_from_api',scope="session")
def get_ingredients_from_api():
    _print_info('\nПолучаем данные об ингредиентах ...')
    response = try_to_get_ingredients()
    # проверяем что получен код ответа 200
    ingredients = check_ingredients_list(response)
    buns_list = get_buns_list(ingredients)
    fillings_list = get_fillings_list(ingredients)
    sauces_list = get_sauces_list(ingredients)

    return buns_list, fillings_list, sauces_list

