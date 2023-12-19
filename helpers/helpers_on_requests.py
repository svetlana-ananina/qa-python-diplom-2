import requests
import allure

from data import SERVER_URL, LOGIN_USER
from data import CREATE_USER, DELETE_USER
from data import _to_print
from helpers.helpers_on_check_response import _print_info, _print_response


@allure.step('Отправляем API-запрос на создание пользователя')
def request_on_create_user(payload):
    # отправляем запрос на создание пользователя курьера и возвращаем ответ
    request_url = f'{SERVER_URL}{CREATE_USER}'
    _print_info(f'\nОтправляем запрос на создание пользователя: POST url="{request_url}" json="{payload}"')
    response = requests.post(f'{request_url}', json=payload)
    _print_response(response)
    return response


@allure.step('Отправляем API-запрос на авторизацию пользователя')
def request_on_login_user(payload):
    # отправляем запрос на авторизацию пользователя и возвращаем ответ
    request_url = f'{SERVER_URL}{LOGIN_USER}'
    _print_info(f'\nОтправляем запрос на авторизацию пользователя: POST url="{request_url}" json="{payload}"')
    response = requests.post(f'{request_url}', json=payload)
    _print_response(response)
    return response


@allure.step('Отправляем API-запрос на удаление пользователя')
def request_on_delete_user(payload):
    # отправляем запрос на удаление пользователя и возвращаем ответ
    request_url = f'{SERVER_URL}{DELETE_USER}'
    _print_info(f'\nОтправляем запрос на удаление пользователя: DELETE url="{request_url}" json="{payload}"')
    response = requests.delete(f'{request_url}', json=payload)
    _print_response(response)
    return response


