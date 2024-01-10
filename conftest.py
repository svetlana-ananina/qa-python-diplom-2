import allure
import pytest

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_get_ingredients import HelpersOnGetIngredients as g


# Получаем данные об ингредиентах от API
@allure.title('Получаем данные об ингредиентах')
@pytest.fixture(scope="session")
def get_ingredients_from_api():
    return c.check_ingredients_list(g.try_to_get_ingredients())

