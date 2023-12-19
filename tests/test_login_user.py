import pytest
import allure

from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from data import RESPONSE_MESSAGES as text

from helpers.helpers_on_check_response import check_status_code, check_success, check_message, check_new_user_data
from helpers.helpers_on_check_response import _print_info
from helpers.helpers_on_create_user import generate_random_user_data, try_to_delete_user, create_user, try_to_login_user


class TestLoginUser:

    def setup(self):
        """
        Инициализируем данные пользователя для удаления после завершения работы
        """
        _print_info(f'\nSetup "TestLoginUser" ...')
        self.to_teardown = False        # Выполнять удаление созданного пользователя
        self.user_data = None
        self.auth_token = None
        self.refresh_token = None

    def teardown(self):
        """
        Удаляем созданного пользователя
        """
        _print_info(f'\nTeardown "TestLoginUser" ...')
        _print_info(f'self.to_teardown={self.to_teardown}')
        if self.to_teardown:
            try_to_delete_user(self.auth_token)

    def init_teardown(self, user_data, auth_token, refresh_token):
        # сохраняем полученные данные пользователя
        self.user_data = user_data.copy()
        self.to_teardown = True
        self.auth_token = auth_token
        self.refresh_token = refresh_token

    @allure.title('Проверка авторизации пользователя под существующим пользователем')
    def test_login_user_success(self):
        # генерируем данные нового пользователя: email, password, user_name
        user_data = generate_random_user_data()
        # отправляем запрос на создание пользователя
        auth_token, refresh_token = create_user(user_data)
        # сохраняем полученные данные пользователя
        self.init_teardown(user_data, auth_token, refresh_token)

        # отправляем запрос на авторизацию пользователя
        response = try_to_login_user(user_data[KEYS.EMAIL_KEY], user_data[KEYS.PASSWORD_KEY])

        # проверяем что получен код ответа 200
        check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = check_success(response, True)
        # проверяем полученные данные в теле ответа
        check_new_user_data(received_body, user_data)

    @allure.title('Проверка авторизации пользователя с неверным логином или паролем')
    @pytest.mark.parametrize('field', [         # неверное поле
        KEYS.EMAIL_KEY,
        KEYS.PASSWORD_KEY
    ])
    def test_login_user_invalid_login_or_password_error(self, field):
        # генерируем данные нового пользователя: email, password, user_name
        user_data = generate_random_user_data()
        # отправляем запрос на создание пользователя
        auth_token, refresh_token = create_user(user_data)
        # сохраняем полученные данные пользователя
        self.init_teardown(user_data, auth_token, refresh_token)
        # формируем данные для авторизации с неверным полем field
        new_user_data = user_data.copy()
        new_user_data[field] = ""

        # отправляем запрос на авторизацию пользователя
        response = try_to_login_user(new_user_data[KEYS.EMAIL_KEY], new_user_data[KEYS.PASSWORD_KEY])

        # проверяем что получен код ответа 401
        check_status_code(response, CODE.UNAUTHORIZED)
        # проверяем в теле ответа: { "success" = False }
        received_body = check_success(response, False)
        # проверяем сообщение в теле ответа: { "message" = "email or password are incorrect" }
        check_message(received_body, text.INVALID_LOGIN)


