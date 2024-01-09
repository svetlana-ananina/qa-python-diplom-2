import allure
import pytest

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_get_ingredients import HelpersOnGetIngredients as g


# Получаем данные об ингредиентах от API
@allure.title('Получаем данные об ингредиентах')
@pytest.fixture(scope="session")
def get_ingredients_from_api():
    return c.check_ingredients_list(g.try_to_get_ingredients())


@allure.title('Получаем список булок')
@pytest.fixture(scope="session")
def get_buns_list_from_api(get_ingredients_from_api):
    return g.get_buns_list(get_ingredients_from_api)


@allure.title('Получаем список начинок')
@pytest.fixture(scope="session")
def get_fillings_list_from_api(get_ingredients_from_api):
    return g.get_fillings_list(get_ingredients_from_api)


@allure.title('Получаем список соусов')
@pytest.fixture(scope="session")
def get_sauces_list_from_api(get_ingredients_from_api):
    return g.get_sauces_list(get_ingredients_from_api)

