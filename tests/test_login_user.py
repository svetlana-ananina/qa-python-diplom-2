import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message
from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_create_user import HelpersOnCreateUser as u


@pytest.fixture
@allure.title('Инициализируем данные пользователя для удаления после завершения работы')
def setup_user():
    # генерируем данные нового пользователя: email, password, user_name
    user_data = u.generate_random_user_data()
    # отправляем запрос на создание пользователя
    auth_token, refresh_token = u.create_user(user_data)
    # сохраняем полученные данные пользователя
    yield auth_token

    # Удаляем созданного пользователя
    u.try_to_delete_user(auth_token)


class TestLoginUser:

    @allure.title('Проверка авторизации пользователя под существующим пользователем')
    def test_login_user_success(self, __setup_user):
        # отправляем запрос на авторизацию пользователя
        response = u.try_to_login_user(self.user_data[KEYS.EMAIL_KEY], self.user_data[KEYS.PASSWORD_KEY])

        # проверяем что получен код ответа 200
        c.check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = c.check_success(response, True)
        # проверяем полученные данные в теле ответа
        c.check_new_user_data(received_body, self.user_data)


    @allure.title('Проверка авторизации пользователя с неверным логином или паролем')
    @pytest.mark.parametrize('field', [         # неверное поле
        KEYS.EMAIL_KEY,
        KEYS.PASSWORD_KEY
    ])
    def test_login_user_invalid_login_or_password_error(self, __setup_user, field):
        # формируем данные для авторизации с неверным полем field
        new_user_data = self.user_data.copy()
        new_user_data[field] = ""

        # отправляем запрос на авторизацию пользователя
        response = u.try_to_login_user(new_user_data[KEYS.EMAIL_KEY], new_user_data[KEYS.PASSWORD_KEY])

        # проверяем что получен код ответа 401
        # проверяем в теле ответа: { "success" = False }
        # проверяем сообщение в теле ответа: { "message" = "email or password are incorrect" }
        c.check_not_success_error_message(response, CODE.UNAUTHORIZED, message.INVALID_LOGIN)


