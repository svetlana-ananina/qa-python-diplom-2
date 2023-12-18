import random
import string

import requests
import allure

from helpers_on_requests import request_on_create_user, request_on_delete_user

from data import STATUS_CODES as code, _to_print
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
@allure.step('Генерируем данные нового пользователя: email, password, user_name')
def generate_random_user_data():
    email = generate_random_string(10)+'@mail.ru'
    password = generate_random_string(10)
    user_name = generate_random_string(10)
    # собираем тело запроса
    user_data = {
        "email": email,
        "password": password,
        "name": user_name
    }
    # возвращаем словарь
    return user_data


# Логирование - вывод в <stdout>
def _print_response(response):
    if _to_print:
        print(f'response="{response}", response.text="{response.text}"')


def _print_response_value(name, value):
    if _to_print:
        print(f'{name}="{value}"')


def _print_info(info_str):
    if _to_print:
        print(info_str)


# метод создания нового курьера, возвращает данные нового курьера: логин, пароль и имя
@allure.title('Создаем нового курьера')
def create_user():
    _print_info('\nСоздаем нового пользователя ...')
    user_data = generate_random_user_data()
    response = request_on_create_user(user_data)


    #_print_info('\nЗапуск фикстуры "create_new_courier()"...')
    # собираем тело запроса = данные нового курьера
    #user_data = generate_random_courier_data()
    # отправляем запрос на создание нового курьера и сохраняем ответ в переменную response
    #response = create_courier(user_data)
    # проверяем что получен код ответа 201
    #check_status_code(response, code.CREATED)
    # проверяем тело ответа:   {'ok' = True}
    #check_key_and_value_in_body(response, KEYS.OK_KEY, True)
    # возвращаем ответ API и данные пользователя
    #_print_info('\nОкончание работы фикстуры create_new_courier()"...')
    #yield user_data
    pass


