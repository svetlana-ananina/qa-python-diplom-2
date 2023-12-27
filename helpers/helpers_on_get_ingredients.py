import pytest
import allure

from data import RESPONSE_KEYS as KEYS
from helpers.helpers_on_check_response import _print_info,check_ingredients_list
from helpers.helpers_on_requests import request_on_get_ingredients


#
# Вспомогательные методы для работы с ингредиентами
@allure.step('Отправляем запрос на получение списка ингредиентов от API')
def try_to_get_ingredients():
    # Отправляем запрос на получение списка ингредиентов
    _print_info('\nПолучаем данные об ингредиентах ...')
    response = request_on_get_ingredients()
    return response


@allure.step('Получаем списки булок из общего списка ингредиентов')
def get_buns_list(ingredients):
    buns_list = []
    for item in ingredients:
        _print_info(f'item={item}')
        if item['type'] == 'bun':
            buns_list.append(item)
    _print_info(f'len(buns_list) = {len(buns_list)}')
    return buns_list


@allure.step('Получаем списки начинок из общего списка ингредиентов')
def get_fillings_list(ingredients):
    fillings_list = []
    for item in ingredients:
        if item['type'] == 'main':
            fillings_list.append(item)
    _print_info(f'len(fillings_list) = {len(fillings_list)}')
    return fillings_list


@allure.step('Получаем списки соусов из общего списка ингредиентов')
def get_sauces_list(ingredients):
    sauces_list = []
    for item in ingredients:
        if item['type'] == 'sauce':
            sauces_list.append(item)
    _print_info(f'len(sauces_list) = {len(sauces_list)}')
    return sauces_list


@allure.step('Создаем список ингредиентов для бургера')
def create_ingredient_list_for_burger(buns_list, fillings_list, sauces_list):
    ingredient_list = [
            (buns_list[0])[KEYS.ID_KEY],
            (fillings_list[0])[KEYS.ID_KEY],
            (sauces_list[0])[KEYS.ID_KEY]
        ]
    _print_info(f'ingredient_list={ingredient_list}')

    return ingredient_list


# Получаем данные об ингредиентах от API
@allure.step('Получаем данные об ингредиентах')
def get_ingredients():
    response = try_to_get_ingredients()
    # проверяем что получен код ответа 200
    ingredients = check_ingredients_list(response)
    return ingredients








