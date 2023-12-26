import allure
import pytest


from helpers.helpers_on_create_user import get_ingredient_list


@pytest.fixture(name='get_ingredient_list_from_api',scope="session")
def get_ingredient_list_from_api():
    # return buns_list, fillings_list, sauces_list
    return get_ingredient_list()
