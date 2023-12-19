import allure
import random
import string

from helpers.helpers_on_check_response import check_status_code, _print_info, check_key_and_value_in_body, \
    check_new_user_data, check_success
from helpers.helpers_on_requests import request_on_create_user, request_on_delete_user, request_on_login_user, \
    request_on_logout_user, request_on_update_user

from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from data import _to_print

# Вспомогательные функции
def generate_random_string(length):
    """
    Метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки.
    :param length: (int) длина строки
    :return: (str) строка
    """
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


# генерируем логин, пароль и имя пользователя
@allure.step('Генерируем данные нового пользователя: email, password, name')
def generate_random_user_data():
    email = generate_random_string(10)+'@mail.ru'
    password = generate_random_string(10)
    name = generate_random_string(10)
    # собираем тело запроса
    user_data = {
        KEYS.EMAIL_KEY: email,            # "email"
        KEYS.PASSWORD_KEY: password,      # "password"
        KEYS.NAME_KEY: name               # "name"
    }
    # возвращаем словарь
    return user_data


@allure.step('Генерируем новое имя пользователя: поле "name"')
def generate_random_user_name():
    return generate_random_string(10)


@allure.step('Генерируем email пользователя: поле "email"')
def generate_random_user_login():
    return generate_random_string(10)+'@mail.ru'


@allure.step('Генерируем пароль пользователя: поле "password"')
def generate_random_user_password():
    return generate_random_string(10)


# метод создания нового пользователя и проверки полученного ответа
def create_and_check_user(user_data=None):
    # генерируем уникальные данные нового пользователя
    if user_data is None:
        user_data = generate_random_user_data()
    # отправляем запрос на создание пользователя
    response = try_to_create_user(user_data)
    # проверяем что получен код ответа 200
    check_status_code(response, CODE.OK)
    # проверяем в теле ответа: { "success" = True }
    received_body = check_success(response, True)
    # проверяем полученные данные пользователя и возвращаем 2 токена
    auth_token, refresh_token = check_new_user_data(received_body, user_data)
    return auth_token, refresh_token


# вспомогательный метод создания нового пользователя для других тестов
def create_user(user_data=None):
    # генерируем уникальные данные нового пользователя
    if user_data is None:
        user_data = generate_random_user_data()
    # отправляем запрос на создание пользователя
    response = try_to_create_user(user_data)
    # проверяем что получен код ответа 200
    check_status_code(response, CODE.OK)
    # проверяем полученные данные и возвращаем 2 токена
    # auth_token, refresh_token = check_user_data(response, email, name)
    received_body = response.json()
    auth_token = received_body[KEYS.ACCESS_TOKEN]
    refresh_token = received_body[KEYS.REFRESH_TOKEN]

    return auth_token, refresh_token


@allure.step('Создаем нового пользователя')
def try_to_create_user(user_data):
    _print_info('\nСоздаем/регистрируем нового пользователя ...')
    response = request_on_create_user(user_data)
    return response


@allure.step('Авторизация пользователя')
def try_to_login_user(email, password):
    _print_info('\nАвторизация пользователя ...')
    payload = {KEYS.EMAIL_KEY: email, KEYS.PASSWORD_KEY: password}
    response = request_on_login_user(payload)
    return response


@allure.step('Удаляем пользователя')
def try_to_delete_user(auth_token):
    _print_info('\nУдаляем пользователя ...')
    headers = {KEYS.AUTH_TOKEN: auth_token}
    response = request_on_delete_user(headers)
    return response


@allure.step('Обновляем данные пользователя')
def try_to_update_user(auth_token, user_data):
    _print_info('\nОбновляем данные пользователя ...')
    headers = {KEYS.AUTH_TOKEN: auth_token}
    response = request_on_update_user(headers, user_data)
    return response


@allure.step('Выход пользователя из системы')
def try_to_logout_user(refresh_token):
    _print_info('\nВыход пользователя из системы ...')
    payload = {KEYS.TOKEN: refresh_token}
    response = request_on_logout_user(payload)
    return response


