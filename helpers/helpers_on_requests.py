import requests
import allure

from data import SERVER_URL, LOGIN_USER, LOGOUT_USER, UPDATE_USER
from data import CREATE_USER, DELETE_USER
from data import _to_print
from helpers.helpers_on_check_response import _print_info, _print_response


@allure.step('Отправляем API-запрос на создание пользователя')
def request_on_create_user(payload):
    request_url = f'{SERVER_URL}{CREATE_USER}'
    _print_info(f'\nОтправляем запрос на создание пользователя: POST url="{request_url}"\njson="{payload}"')
    response = requests.post(f'{request_url}', json=payload)
    _print_response(response)
    return response


@allure.step('Отправляем API-запрос на авторизацию пользователя')
def request_on_login_user(payload):
    request_url = f'{SERVER_URL}{LOGIN_USER}'
    _print_info(f'\nОтправляем запрос на авторизацию пользователя: POST url="{request_url}"\njson="{payload}"')
    response = requests.post(f'{request_url}', json=payload)
    _print_response(response)
    return response


@allure.step('Отправляем API-запрос на выход пользователя из системы')
def request_on_logout_user(payload):
    request_url = f'{SERVER_URL}{LOGOUT_USER}'
    _print_info(f'\nОтправляем запрос на выход пользователя из системы: POST url="{request_url}"\njson="{payload}"')
    response = requests.post(f'{request_url}', json=payload)
    _print_response(response)
    return response


@allure.step('Отправляем API-запрос на удаление пользователя')
def request_on_delete_user(headers):
    request_url = f'{SERVER_URL}{DELETE_USER}'
    _print_info(f'\nОтправляем запрос на удаление пользователя: DELETE url="{request_url}"\nheaders="{headers}"')
    response = requests.delete(f'{request_url}', headers=headers)
    _print_response(response)
    return response


@allure.step('Отправляем API-запрос на обновление данных пользователя')
def request_on_update_user(headers, payload):
    request_url = f'{SERVER_URL}{UPDATE_USER}'
    _print_info(f'\nОтправляем запрос на обновление данных пользователя: PATCH url="{request_url}"\nheaders="{headers}"\njson="{payload}"')
    response = requests.patch(f'{request_url}', headers=headers)
    _print_response(response)
    return response


