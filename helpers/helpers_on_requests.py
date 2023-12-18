import requests
import allure

from data import SERVER_URL
from data import CREATE_USER, DELETE_USER
from data import _to_print

from helpers_on_create_user import _print_response, _print_response_value, _print_info


@allure.step('Отправляем API-запрос на создание пользователя')
def request_on_create_user(payload):
    # отправляем запрос на создание курьера и возвращаем ответ
    request_url = f'{SERVER_URL}{CREATE_USER}'
    _print_info(f'\nОтправляем запрос на создание пользователя: POST url="{request_url}" json="{payload}"')
    response = requests.post(f'{request_url}', json=payload)
    _print_response(response)
    return response


@allure.step('Отправляем API-запрос на удаление пользователя')
def request_on_delete_user(payload):
    # отправляем запрос на создание курьера и возвращаем ответ
    request_url = f'{SERVER_URL}{DELETE_USER}'
    _print_info(f'\nОтправляем запрос на удаление пользователя: DELETE url="{request_url}" json="{payload}"')
    response = requests.delete(f'{request_url}', json=payload)
    _print_response(response)
    return response


