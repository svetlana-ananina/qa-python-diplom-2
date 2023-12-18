import allure

from data import STATUS_CODES as code, _to_print
from data import RESPONSE_KEYS as KEYS


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


