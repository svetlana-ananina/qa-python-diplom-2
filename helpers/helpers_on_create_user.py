import allure
import pytest
import random
import string

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_requests import Requests as r

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS


class HelpersOnCreateUser:
    # Вспомогательные функции

    @staticmethod
    def generate_random_string(length):
        """
        Метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки.
        :param length: (int) длина строки
        :return: (str) строка
        """
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string


    @staticmethod
    @allure.step('Отправляем запрос на создание нового пользователя')
    def try_to_create_user(user_data):
        return r.request_on_create_user(user_data)


    @staticmethod
    @allure.step('Авторизация пользователя')
    def try_to_login_user(email, password):
        payload = {KEYS.EMAIL_KEY: email, KEYS.PASSWORD_KEY: password}
        return r.request_on_login_user(payload)


    @staticmethod
    @allure.step('Удаляем пользователя')
    def try_to_delete_user(auth_token):
        headers = {KEYS.AUTH_TOKEN_KEY: auth_token}
        return r.request_on_delete_user(headers)


    @staticmethod
    @allure.step('Обновляем данные пользователя')
    def try_to_update_user(user_data, auth_token=None):
        if auth_token is not None:
            headers = {KEYS.AUTH_TOKEN_KEY: auth_token}
        else:
            headers = None
        return r.request_on_update_user(user_data, headers)


    @staticmethod
    @allure.step('Выход пользователя из системы')
    def try_to_logout_user(token):
        payload = {KEYS.TOKEN_KEY: token}
        return r.request_on_logout_user(payload)


    # Вспомогательные методы для работы с заказами
    @staticmethod
    @allure.step('Отправляем запрос на создание заказа')
    def try_to_create_order(ingredient_list, auth_token=None):  # ingredient_list - список _id ингредиентов
        if auth_token is not None:
            headers = {
                KEYS.AUTH_TOKEN_KEY: auth_token,  # "Autorization": auth_token
            }
        else:
            headers = None

        payload = {
            KEYS.INGREDIENTS: ingredient_list,  # "ingredients": ingredient_list,
        }
        return r.request_on_create_order(payload, headers)


    @staticmethod
    @allure.step('Отправляем запрос на получение заказов пользователя')
    def try_to_get_user_orders(auth_token=None):
        if auth_token is not None:
            headers = {
                KEYS.AUTH_TOKEN_KEY: auth_token,  # "Autorization": auth_token
            }
        else:
            headers = None
        return r.request_on_get_user_orders(headers)


    # генерируем логин, пароль и имя пользователя
    @staticmethod
    @allure.step('Генерируем данные нового пользователя: email, password, name')
    def generate_random_user_data():
        email = HelpersOnCreateUser.generate_random_string(10) + '@mail.ru'
        password = HelpersOnCreateUser.generate_random_string(10)
        name = HelpersOnCreateUser.generate_random_string(10)
        # собираем тело запроса
        user_data = {
            KEYS.EMAIL_KEY: email,  # "email"
            KEYS.PASSWORD_KEY: password,  # "password"
            KEYS.NAME_KEY: name  # "name"
        }
        # возвращаем словарь
        return user_data


    @staticmethod
    @allure.step('Генерируем новое имя пользователя: поле "name"')
    def generate_random_user_name():
        return HelpersOnCreateUser.generate_random_string(10)


    @staticmethod
    @allure.step('Генерируем email пользователя: поле "email"')
    def generate_random_user_login():
        return HelpersOnCreateUser.generate_random_string(10) + '@mail.ru'


    @staticmethod
    @allure.step('Генерируем пароль пользователя: поле "password"')
    def generate_random_user_password():
        return HelpersOnCreateUser.generate_random_string(10)


    # метод создания нового пользователя и проверки полученного ответа
    @staticmethod
    @allure.step('Создаем нового пользователя')
    def create_and_check_user(user_data=None):
        # генерируем уникальные данные нового пользователя
        if user_data is None:
            user_data = HelpersOnCreateUser.generate_random_user_data()
        # отправляем запрос на создание пользователя
        response = HelpersOnCreateUser.try_to_create_user(user_data)
        # проверяем что получен код ответа 200
        # проверяем в теле ответа: { "success" = True }
        received_body = c.check_success(response, True)
        # проверяем полученные данные пользователя и возвращаем 2 токена
        auth_token, refresh_token = c.check_new_user_data(received_body, user_data)
        return auth_token, refresh_token


    # вспомогательный метод создания нового пользователя для других тестов
    @staticmethod
    @allure.step('Создаем нового пользователя')
    def create_user(user_data=None):
        # генерируем уникальные данные нового пользователя
        if user_data is None:
            user_data = HelpersOnCreateUser.generate_random_user_data()
        # отправляем запрос на создание пользователя
        response = HelpersOnCreateUser.try_to_create_user(user_data)
        # проверяем что получен код ответа 200
        c.check_status_code(response, CODE.OK)
        # получаем токены пользователя
        received_body = response.json()
        auth_token = received_body[KEYS.ACCESS_TOKEN]
        refresh_token = received_body[KEYS.REFRESH_TOKEN]
        return auth_token, refresh_token


    # Вспомогательные методы для работы с заказами
    @staticmethod
    @allure.step('Создаем заказ и проверяем полученные в ответе данные')
    def create_order(ingredient_list, auth_token=None):
        # создаем заказ
        response = HelpersOnCreateUser.try_to_create_order(ingredient_list, auth_token)
        # проверяем что получен код ответа 200
        c.check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = c.check_success(response, True)
        # Получаем данные заказа - name, number
        order_name = c.check_key_in_body(received_body, KEYS.NAME_KEY)
        received_order_data = c.check_key_in_body(received_body, KEYS.ORDER_KEY)
        order_number = c.check_key_in_body(received_order_data, KEYS.NUMBER_KEY)

        return order_number, order_name

