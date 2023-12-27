import pytest
import allure

from conftest import get_ingredients_from_api, get_buns_list_from_api, get_fillings_list_from_api, \
    get_sauces_list_from_api
from helpers.helpers_on_check_response import _print_info


#@pytest.mark.usefixtures('get_ingredients_from_api, get_buns_list_from_api')
@pytest.mark.usefixtures('get_ingredients_from_api')
#@pytest.mark.usefixtures('get_buns_list_from_api')
class MyIngredientsList:
    #ingredients = None
    #buns_list = []
    #fillings_list = []
    #sauces_list = []
    buns_list = get_buns_list_from_api
    fillings_list = get_fillings_list_from_api
    sauces_list = get_sauces_list_from_api

    #@pytest.mark.usefixtures('get_ingredients_from_api')
    #@pytest.mark.usefixtures('get_buns_list_from_api')
    #@classmethod
    #def setup(cls, get_buns_list_from_api, get_fillings_list_from_api, get_sauces_list_from_api):
    #    _print_info('MyIngredientsList setup method ...')
    #    #cls.ingredients = get_ingredients_from_api
    #    cls.buns_list = get_buns_list_from_api.copy()
    #    cls.fillings_list = get_fillings_list_from_api.copy()
    #    cls.sauces_list = get_sauces_list_from_api.copy()

    @classmethod
    def get_buns_list(cls):
        return list(cls.buns_list)

    @classmethod
    def get_fillings_list(cls):
        return list(cls.fillings_list)

    @classmethod
    def get_sauces_list(cls):
        return list(cls.sauces_list)


