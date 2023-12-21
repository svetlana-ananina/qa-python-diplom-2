import allure
import random
import string

from helpers.helpers_on_check_response import check_status_code, _print_info, check_new_user_data, check_success, \
    check_key_in_body
from helpers.helpers_on_requests import request_on_create_user, request_on_delete_user, request_on_login_user, \
    request_on_logout_user, request_on_update_user, request_on_reset_password, request_on_get_ingredients, \
    request_on_create_order

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
def try_to_update_user(user_data, auth_token=None):
    _print_info('\nОбновляем данные пользователя ...')
    if auth_token is not None:
        headers = {KEYS.AUTH_TOKEN: auth_token}
    else:
        headers = None
    response = request_on_update_user(user_data, headers)
    return response


@allure.step('Выход пользователя из системы')
def try_to_logout_user(token):
    _print_info('\nВыход пользователя из системы ...')
    payload = {KEYS.TOKEN: token}
    response = request_on_logout_user(payload)
    return response


@allure.step('Устанавливаем новый пароль пользователя')
def try_to_reset_password(new_password, token):
    _print_info('\nУстанавливаем новый пароль пользователя ...')
    payload = {
        KEYS.PASSWORD_KEY: new_password,
        KEYS.TOKEN: token
    }
    response = request_on_reset_password(payload)
    return response


@allure.step('Получаем данные об ингредиентах')
def try_to_get_ingredients():
    _print_info('\nПолучаем данные об ингредиентах ...')
    response = request_on_get_ingredients()
    return response


@allure.step('Получаем данные об ингредиентах')
def get_ingredients():
    response = try_to_get_ingredients()
    # проверяем что получен код ответа 200
    check_status_code(response, CODE.OK)
    # проверяем в теле ответа: { "success" = True }
    received_body = check_success(response, True)
    # проверяем наличие в ответе ключа "data" и получаем его значение - список ингредиентов (словарь)
    ingredients = check_key_in_body(received_body, KEYS.DATA)
    # проверяем что поле data содержит список и возвращаем его
    assert type(ingredients) is list and len(ingredients) > 0
    return ingredients


@allure.step('Получаем списки булок из общего списка ингредиентов')
def get_buns_list(ingredients):
    buns_list = []
    for item in ingredients:
        _print_info(f'item={item}')
        # item_type = item['type']
        # _print_info(f"item['type']={item['type']}")
        # _print_info(f"item['type'] == 'bun' = {item['type'] == 'bun'}")
        if item['type'] == 'bun':
        # if item_type == 'bun':
            buns_list.append(item)
    _print_info(f'len(buns_list) = {len(buns_list)}')
    _print_info(f'buns_list={buns_list}')
    return buns_list


@allure.step('Получаем списки начинок из общего списка ингредиентов')
def get_fillings_list(ingredients):
    fillings_list = []
    for item in ingredients:
        if item['type'] == 'main':
            fillings_list.append(item)
    _print_info(f'len(fillings_list) = {len(fillings_list)}')
    _print_info(f'fillings_list={fillings_list}')
    return fillings_list


@allure.step('Получаем списки соусов из общего списка ингредиентов')
def get_sauces_list(ingredients):
    sauces_list = []
    for item in ingredients:
        if item['type'] == 'sauce':
            sauces_list.append(item)
    _print_info(f'len(sauces_list) = {len(sauces_list)}')
    _print_info(f'sauces_list={sauces_list}')
    return sauces_list


@allure.step('Создаем заказ')
def try_to_create_order(ingredient_list, auth_token=None):      # ingredient_list - список _id ингредиентов
    _print_info('\nСоздаем заказ ...')
    if auth_token is not None:
        headers = {KEYS.AUTH_TOKEN: auth_token}
    else:
        headers = None
    payload = '{' + f'"{KEYS.INGREDIENTS}":{ingredient_list}' + '}'
    response = request_on_create_order(payload, headers)
    return response


