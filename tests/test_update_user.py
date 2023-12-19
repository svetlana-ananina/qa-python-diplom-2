import pytest
import allure

from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from data import RESPONSE_MESSAGES as text

from helpers.helpers_on_check_response import check_status_code, check_success, check_user_data
from helpers.helpers_on_check_response import _print_info
from helpers.helpers_on_create_user import generate_random_user_data, try_to_delete_user, create_user, \
    try_to_update_user, generate_random_user_name, generate_random_user_login


class TestUpdateUser:

    def setup(self):
        """
        Инициализируем данные пользователя для удаления после завершения работы
        """
        _print_info(f'\nSetup "TestLoginUser" ...')
        self.to_teardown = False        # Выполнять удаление созданного пользователя
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

    def init_teardown(self, auth_token, refresh_token):
        # сохраняем полученные данные пользователя
        self.to_teardown = True
        self.auth_token = auth_token
        self.refresh_token = refresh_token

    @allure.title('Проверка обновления данных пользователя')
    @pytest.mark.parametrize('field', [         # обновляемое поле
        KEYS.EMAIL_KEY,
        KEYS.PASSWORD_KEY,
        KEYS.NAME_KEY
    ])
    def test_update_user_success(self, field):
        # генерируем данные нового пользователя: email, password, user_name
        user_data = generate_random_user_data()
        # отправляем запрос на создание пользователя
        auth_token, refresh_token = create_user(user_data)
        # сохраняем полученные данные пользователя
        self.init_teardown(auth_token, refresh_token)

        # генерируем новые данные пользователя в поле field
        if field is KEYS.EMAIL_KEY:
            new_field_data = generate_random_user_login()
        else:
            new_field_data = generate_random_user_name()
        # формируем тело запроса для обновления поля field
        payload = {
            field: new_field_data
        }
        # сохраняем новые данные пользователя
        new_user_data = user_data.copy()
        new_user_data[field] = new_field_data

        # отправляем запрос на изменение данных пользователя
        response = try_to_update_user(auth_token, payload)

        # проверяем что получен код ответа 200
        check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = check_success(response, True)
        # проверяем полученные данные пользователя в теле ответа - поле "user"
        check_user_data(received_body, new_user_data)

