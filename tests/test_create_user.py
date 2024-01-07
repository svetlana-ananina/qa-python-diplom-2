import pytest
import allure

from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from data import RESPONSE_MESSAGES as text

from helpers.helpers_on_check_response import _print_info, check_not_success_error_message
from helpers.helpers_on_create_user import generate_random_user_data, create_and_check_user, try_to_create_user, \
    try_to_delete_user, create_user


class TestCreateUser:

    def setup_method(self):
        """
        Инициализируем данные пользователя для удаления после завершения работы
        """
        _print_info(f'\nsetup_method "TestCreateUser" ...')
        self.to_teardown = False        # Выполнять удаление созданного пользователя
        self.user_data = None
        self.auth_token = None
        self.refresh_token = None

    def teardown_method(self):
        """
        Удаляем созданного пользователя
        """
        _print_info(f'\nteardown_method "TestCreateUser" ...')
        _print_info(f'self.to_teardown={self.to_teardown}')
        if self.to_teardown:
            try_to_delete_user(self.auth_token)

    def init_teardown(self, user_data, auth_token, refresh_token):
        """
        сохраняем полученные данные пользователя
        """
        self.user_data = user_data.copy()
        self.to_teardown = True
        self.auth_token = auth_token
        self.refresh_token = refresh_token

    @allure.title('Проверка создания пользователя - регистрация уникального пользователя')
    def test_create_user_new_user(self):
        # генерируем уникальные данные нового пользователя: email, password, user_name
        user_data = generate_random_user_data()

        # отправляем запрос на создание пользователя и проверяем полученные данные
        auth_token, refresh_token = create_and_check_user(user_data)

        # сохраняем полученные данные пользователя
        self.init_teardown(user_data, auth_token, refresh_token)

    @allure.title('Проверка создания пользователя - повторная регистрация пользователя')
    def test_create_user_double_user_error(self):
        # генерируем уникальные данные нового пользователя: email, password, user_name
        user_data = generate_random_user_data()
        # отправляем запрос на создание пользователя
        auth_token, refresh_token = create_user(user_data)
        # сохраняем полученные данные пользователя
        self.init_teardown(user_data, auth_token, refresh_token)

        # отправляем повторный запрос на создание того же пользователя
        response = try_to_create_user(user_data)

        # проверяем что получен код ответа 403
        # проверяем в теле ответа: { "success" = False }
        # проверяем сообщение в теле ответа: { "message" = "User already exists" }
        check_not_success_error_message(response, CODE.FORBIDDEN, text.USER_ALREADY_EXISTS)

    @allure.title('Проверка создания пользователя - не заполнено одно из полей')
    @pytest.mark.parametrize('field', [         # незаполненное поле
        KEYS.EMAIL_KEY,
        KEYS.PASSWORD_KEY,
        KEYS.NAME_KEY
    ])
    def test_create_user_empty_field_error(self, field):
        # генерируем уникальные данные нового пользователя: email, password, user_name
        user_data = generate_random_user_data()
        # удаляем поле field
        user_data.pop(field)

        # отправляем запрос на создание пользователя
        response = try_to_create_user(user_data)

        # проверяем что получен код ответа 403
        # проверяем в теле ответа: { "success" = False }
        # проверяем сообщение в теле ответа: { "message" = "Email, password and name are required fields" }
        check_not_success_error_message(response, CODE.FORBIDDEN, text.MISSING_REQUIRED_FIELD)

