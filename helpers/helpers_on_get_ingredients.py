import pytest
import allure

from data import ResponseKeys as KEYS
from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_requests import Requests as r


#
# Вспомогательные методы для работы с ингредиентами
class HelpersOnGetIngredients:

    @staticmethod
    @allure.step('Отправляем запрос на получение списка ингредиентов от API')
    def try_to_get_ingredients():
        # Отправляем запрос на получение списка ингредиентов
        return r.request_on_get_ingredients()


    @staticmethod
    @allure.step('Получаем списки булок из общего списка ингредиентов')
    def get_buns_list(ingredients):
        buns_list = []
        for item in ingredients:
            if item['type'] == 'bun':
                buns_list.append(item)
        return buns_list


    @staticmethod
    @allure.step('Получаем списки начинок из общего списка ингредиентов')
    def get_fillings_list(ingredients):
        fillings_list = []
        for item in ingredients:
            if item['type'] == 'main':
                fillings_list.append(item)
        return fillings_list


    @staticmethod
    @allure.step('Получаем списки соусов из общего списка ингредиентов')
    def get_sauces_list(ingredients):
        sauces_list = []
        for item in ingredients:
            if item['type'] == 'sauce':
                sauces_list.append(item)
        return sauces_list


    # Получаем данные об ингредиентах от API
    @staticmethod
    @allure.step('Получаем данные об ингредиентах')
    def get_ingredients():
        response = HelpersOnGetIngredients.try_to_get_ingredients()
        # проверяем что получен код ответа 200
        return c.check_ingredients_list(response)

