import allure
import random
import string

from helpers.helpers_on_check_response import check_status_code, _print_info, check_key_and_value_in_body, \
    check_user_data, check_success
from helpers.helpers_on_requests import request_on_create_user, request_on_delete_user, request_on_login_user

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


# метод создания нового пользователя и проверки полученного ответа
#@allure.step('Создаем нового пользователя')
def create_and_check_user(user_data=None):
    # генерируем уникальные данные нового пользователя
    if user_data is None:
        user_data = generate_random_user_data()
    # отправляем запрос на создание пользователя
    response = try_to_create_user(user_data)
    # проверяем что получен код ответа 200
    check_status_code(response, CODE.OK)
    # проверяем в теле ответа: { "success" = True }
    # check_key_and_value_in_body(response, KEYS.SUCCESS_KEY, True)
    check_success(response, True)
    # возвращаем данные пользователя в теле ответа
    email = user_data[KEYS.EMAIL_KEY]
    name = user_data[KEYS.NAME_KEY]
    # проверяем полученные данные и возвращаем 2 токена
    user_token, refresh_token = check_user_data(response, email, name)
    return user_token, refresh_token


@allure.step('Создаем нового пользователя')
def try_to_create_user(user_data):
    _print_info('\nСоздаем/регистрируем нового пользователя ...')
    response = request_on_create_user(user_data)
    return response


@allure.step('Авторизация пользователя')
def try_to_login_user(email, password):
    _print_info('\nАвторизация пользователя ...')
    payload = {KEYS.EMAIL_KEY: email, KEYS.PASSWORD_KEY: password}
    # отправляем запрос на авторизацию пользователя
    response = request_on_login_user(payload)
    return response


@allure.step('Удаляем пользователя')
def try_to_delete_user(aurh_token):
    _print_info('\nУдаляем пользователя ...')
    payload = {KEYS.AUTH_TOKEN: aurh_token}
    response = request_on_delete_user(payload)
    return response




