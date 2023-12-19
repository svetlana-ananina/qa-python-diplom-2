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
@allure.step('Проверяем код ответа')
def check_status_code(response, expected_code):
    # проверяем что получен код ответа expected_code
    received_code = response.status_code
    assert received_code == expected_code, f'Неверный код в ответе: ожидался {expected_code}, получен "{received_code}", ответ: "{response.text}"'


@allure.step('Проверяем сообщение в ответе')
def check_message(response, expected_message):
    # проверяем что в ответе есть message
    received_text = response.text
    received_body = response.json()
    assert KEYS.MESSAGE_KEY in received_body, f'В ответе отсутствует ключ "{KEYS.MESSAGE_KEY}", текст: "{received_text}"'
    # проверяем сообщение об ошибке
    received_message = received_body[KEYS.MESSAGE_KEY]
    assert received_message == expected_message, f'Получено неверное сообщение: ожидалось: "{expected_message}", получено: "{received_message}"'


@allure.step('Проверяем наличие ключа в ответе')
def check_key_in_body(response, key):
    # проверяем что в ответе есть ключ key
    received_text = response.text
    assert key in response.json(), f'В ответе отсутствует ключ "{key}", получен ответ: "{received_text}"'
    return response.json()[key]


@allure.step('Проверяем значение ключа в ответе')
def check_key_and_value_in_body(response, key, value):
    received_text = response.text
    received_body = response.json()
    # проверяем наличие ключа в ответе
    assert key in received_body, f'В ответе отсутствует ключ "{key}", получен ответ: "{received_text}"'
    # проверяем значение ключа в ответе
    assert received_body[key] == value, f'Получено неверное значение ключа: ожидалось: "{key}" = "{value}", текст: "{received_text}"'


#
# Проверка данных пользователя после создания пользователя
@allure.step('Проверяем полученные данные пользователя после регистрации')
def check_user_data(response, email, name):
    received_text = response.text

    # проверяем наличие в ответе ключа "user" и получаем его значение - словарь
    received_user_data = check_key_in_body(response, KEYS.USER_KEY)
    assert type(received_user_data) is dict

    # проверяем наличие в словаре "user" полей "email" и "name"
    assert KEYS.EMAIL_KEY in received_user_data, f'В ответе отсутствует ключ "{KEYS.EMAIL_KEY}", получен ответ: "{received_text}"'
    assert KEYS.NAME_KEY in received_user_data, f'В ответе отсутствует ключ "{KEYS.NAME_KEY}", получен ответ: "{received_text}"'
    received_user_email = received_user_data[KEYS.EMAIL_KEY]
    received_user_name = received_user_data[KEYS.NAME_KEY]
    assert received_user_email == email, f'Получено неверное значение ключа "{KEYS.NAME_KEY}": ожидалось "{name}", получено "{received_user_email}"'
    assert received_user_name == name, f'Получено неверное значение ключа "{KEYS.NAME_KEY}": ожидалось "{name}", получено "{received_user_name}"'

    # проверяем наличие в ответе ключа "accessToken" и получаем его значение - строку
    user_token = check_key_in_body(response, KEYS.ACCESS_TOKEN)
    # проверяем формат токена: "Bearer ..."
    assert (type(user_token) is str and
            ACCESS_TOKEN_PREFIX in user_token and
            len(user_token) > len(ACCESS_TOKEN_PREFIX)), f'Получено неверное значение ключа "{KEYS.ACCESS_TOKEN}": неправильный формат "{KEYS.ACCESS_TOKEN}"="{user_token}"'

    # проверяем наличие в ответе ключа "refreshToken" и получаем его значение - строку
    refresh_token = check_key_in_body(response, KEYS.REFRESH_TOKEN)
    # проверяем токен
    assert (type(refresh_token) is str and
            len(refresh_token) > 0), f'Получено неверное значение ключа "{KEYS.REFRESH_TOKEN}": неправильный формат "{KEYS.REFRESH_TOKEN}"="{refresh_token}"'

    return user_token, refresh_token


