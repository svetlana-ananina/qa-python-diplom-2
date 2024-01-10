import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message
from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_create_user import HelpersOnCreateUser as u


class TestLoginUser:

    @allure.title('Проверка авторизации пользователя под существующим пользователем')
    def test_login_user_success(self, setup_user):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # отправляем запрос на авторизацию пользователя
        response = u.try_to_login_user(user_data[KEYS.EMAIL_KEY], user_data[KEYS.PASSWORD_KEY])

        # проверяем что получен код ответа 200
        c.check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = c.check_success(response, True)
        # проверяем полученные данные в теле ответа
        c.check_new_user_data(received_body, user_data)


    @allure.title('Проверка авторизации пользователя с неверным логином или паролем')
    @pytest.mark.parametrize('field', [         # неверное поле
        KEYS.PASSWORD_KEY,
        KEYS.EMAIL_KEY,
    ])
    def test_login_user_invalid_login_or_password_error(self, setup_user, field):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # формируем данные для авторизации с неверным полем field
        new_user_data = user_data.copy()
        new_user_data[field] = ""

        # отправляем запрос на авторизацию пользователя
        response = u.try_to_login_user(new_user_data[KEYS.EMAIL_KEY], new_user_data[KEYS.PASSWORD_KEY])

        # проверяем что получен код ответа 401
        # проверяем в теле ответа: { "success" = False }
        # проверяем сообщение в теле ответа: { "message" = "email or password are incorrect" }
        c.check_not_success_error_message(response, CODE.UNAUTHORIZED, message.INVALID_LOGIN)


