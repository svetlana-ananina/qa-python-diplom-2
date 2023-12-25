import allure

from data import STATUS_CODES as code, _to_print, ACCESS_TOKEN_PREFIX
from data import RESPONSE_KEYS as KEYS


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


#
# Вспомогательные методы проверки ответа на запрос к API
#@allure.step('Проверяем наличие ключа в ответе')
def check_key_in_body(response_body, key):
    # проверяем что в ответе есть ключ key
    assert key in response_body, f'В ответе отсутствует ключ "{key}", получен ответ: "{response_body}"'
    return response_body[key]


#@allure.step('Проверяем значение ключа в ответе')
def check_key_and_value_in_body(response_body, key, value):
    # проверяем наличие ключа в ответе
    assert key in response_body, f'В ответе отсутствует ключ "{key}", получен ответ: "{response_body}"'
    # проверяем значение ключа в ответе
    received_value = response_body[key]
    assert received_value == value, f'Получено неверное значение ключа "{key}": ожидалось "{value}", получено "{received_value}"'
    return received_value


@allure.step('Проверяем код ответа')
def check_status_code(response, expected_code):
    # проверяем что получен код ответа expected_code
    received_code = response.status_code
    assert received_code == expected_code, f'Неверный код в ответе: ожидался {expected_code}, получен "{received_code}", ответ: "{response.text}"'


@allure.step('Проверяем значение поля "success" в ответе')
def check_success(response, expected_value):
    received_text = response.text
    # проверяем что в ответе есть "success"
    assert KEYS.SUCCESS_KEY in response.json(), f'В ответе отсутствует ключ "{KEYS.SUCCESS_KEY}", получено: "{received_text}"'
    # проверяем тело ответа
    received_body = response.json()
    # проверяем сообщение об ошибке
    received_value = received_body[KEYS.SUCCESS_KEY]
    assert received_value == expected_value, f'Получено неверное значение поля "{KEYS.SUCCESS_KEY}": ожидалось "{expected_value}", получено "{received_value}"'
    return received_body


@allure.step('Проверяем сообщение в ответе')
def check_message(received_body, expected_message):
    # проверяем что в ответе есть "message"
    assert KEYS.MESSAGE_KEY in received_body, f'В ответе отсутствует ключ "{KEYS.MESSAGE_KEY}", получено: "{received_body}"'
    # проверяем сообщение об ошибке
    received_message = received_body[KEYS.MESSAGE_KEY]
    assert received_message == expected_message, f'Получено неверное значение поля "{KEYS.MESSAGE_KEY}":\nожидалось "{expected_message}"\nполучено "{received_message}"'
    return received_message


@allure.step('Получаем значение ключа')
def get_key_from_body(response_body, key):
    return response_body[key]


#
# Проверка полученных данных пользователя после создания/авторизации пользователя
@allure.step('Проверяем полученные данные пользователя - поле "user"')
def check_user_data(received_body, user_data):
    # проверяем наличие в ответе ключа "user" и получаем его значение - словарь
    received_user_data = check_key_in_body(received_body, KEYS.USER_KEY)
    assert type(received_user_data) is dict

    # проверяем в словаре "user" наличие и значения полей "email" и "name"
    email = user_data[KEYS.EMAIL_KEY]
    name = user_data[KEYS.NAME_KEY]
    check_key_and_value_in_body(received_user_data, KEYS.EMAIL_KEY, email)
    check_key_and_value_in_body(received_user_data, KEYS.NAME_KEY, name)


@allure.step('Проверяем полученные данные пользователя после регистрации/авторизации')
def check_new_user_data(received_body, user_data):
    # проверяем наличие в ответе ключа "user" и значения полей "email" и "name"
    check_user_data(received_body, user_data)

    # проверяем наличие в ответе ключа "accessToken" и получаем его значение - строку "Bearer ..."
    auth_token = check_key_in_body(received_body, KEYS.ACCESS_TOKEN)
    # проверяем формат токена: "Bearer ..."
    assert (type(auth_token) is str and
            ACCESS_TOKEN_PREFIX in auth_token and
            len(auth_token) > len(ACCESS_TOKEN_PREFIX)), f'Получено неверное значение ключа "{KEYS.ACCESS_TOKEN}": неправильный формат "{KEYS.ACCESS_TOKEN}"={auth_token}'

    # проверяем наличие в ответе ключа "refreshToken" и получаем его значение - строку `"..."
    refresh_token = check_key_in_body(received_body, KEYS.REFRESH_TOKEN)
    # проверяем токен
    assert (type(refresh_token) is str and
            len(refresh_token) > 0), f'Получено неверное значение ключа "{KEYS.REFRESH_TOKEN}": неправильный формат "{KEYS.REFRESH_TOKEN}"={refresh_token}'
    # возвращаем полученные токены
    return auth_token, refresh_token


#
# Проверка полученных данных после создания заказа
@allure.step('Проверяем полученные данные пользователя - поле "user"')
def check_order_data(received_body):
    # проверяем наличие в ответе ключа "name" и получаем его значение - строка
    order_name = check_key_in_body(received_body, KEYS.NAME_KEY)
    assert type(order_name) is str, f'Получено неверное значение ключа "{KEYS.NAME_KEY}": ожидалось - строка, получено значение {order_name} тип {type(order_name)}'

    # проверяем наличие в ответе ключа "order" и получаем его значение - словарь
    received_order_data = check_key_in_body(received_body, KEYS.ORDER_KEY)
    assert type(received_order_data) is dict

    # проверяем в словаре "order" наличие и значения поля "number"
    order_number = check_key_in_body(received_order_data, KEYS.NUMBER_KEY)
    assert str(order_number).isdigit(), f'Получено неверное значение ключа "{KEYS.NUMBER_KEY}": ожидалось - число, получено значение {order_number} тип {type(order_number)}'

    return order_number, order_name


