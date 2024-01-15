import requests
import allure

from data import Endpoints as e


class Requests:

    @staticmethod
    @allure.step('Отправляем API-запрос на создание пользователя')
    def request_on_create_user(payload):
        request_url = f'{e.SERVER_URL}{e.CREATE_USER}'
        return requests.post(f'{request_url}', json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на авторизацию пользователя')
    def request_on_login_user(payload):
        request_url = f'{e.SERVER_URL}{e.LOGIN_USER}'
        return requests.post(f'{request_url}', json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на выход пользователя из системы')
    def request_on_logout_user(payload):
        request_url = f'{e.SERVER_URL}{e.LOGOUT_USER}'
        return requests.post(f'{request_url}', json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на удаление пользователя')
    def request_on_delete_user(headers):
        request_url = f'{e.SERVER_URL}{e.DELETE_USER}'
        return requests.delete(f'{request_url}', headers=headers)

    @staticmethod
    @allure.step('Отправляем API-запрос на обновление данных пользователя')
    def request_on_update_user(payload, headers=None):
        request_url = f'{e.SERVER_URL}{e.UPDATE_USER}'
        return requests.patch(f'{request_url}', headers=headers, json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на изменение пароля пользователя')
    def request_on_reset_password(payload):
        request_url = f'{e.SERVER_URL}{e.RESET_PASSWORD}'
        return requests.post(f'{request_url}', json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на получение ингредиентов')
    def request_on_get_ingredients():
        request_url = f'{e.SERVER_URL}{e.GET_INGREDIENTS}'
        return requests.get(f'{request_url}')

    @staticmethod
    @allure.step('Отправляем API-запрос на создание заказа')
    def request_on_create_order(payload, headers=None):
        request_url = f'{e.SERVER_URL}{e.CREATE_ORDER}'
        return requests.post(f'{request_url}', headers=headers, json=payload)

    @staticmethod
    @allure.step('Отправляем API-запрос на получение заказов пользователя')
    def request_on_get_user_orders(headers=None):
        request_url = f'{e.SERVER_URL}{e.GET_USER_ORDERS}'
        return requests.get(f'{request_url}', headers=headers)

