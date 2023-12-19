import pytest
import allure

from helpers.helpers_on_check_response import _print_info
from helpers.helpers_on_create_user import generate_random_user_data, create_and_check_user


class TestCreateUser:

    def setup(self):
        _print_info(f'\nSetup "TestCreateUser" ...')
        self.to_teardown = False
        # self.user_data = None
        # self.is_login = False

    def teardown(self):
        _print_info(f'\nTeardown "TestCreateUser" ...')
        _print_info(f'self.to_teardown={self.to_teardown}')
        # _print_info(f'self.is_login={self.is_login}')
        # if self.to_teardown:
        #     if not self.is_login:
        #         response = try_to_login_user(self.user_data["email"], self.user_data["password"])
        #     auth_token = self.user_data[KEYS.ACCESS_TOKEN]
        #     _print_info(f'\nУдаляем пользователя ...\nauth_token="{auth_token}"')
        #     response = try_to_delete_user(auth_token)

    @allure.title('Создаем нового пользователя')
    def test_create_user(self):
        # генерируем уникальные данные нового пользователя: email, password, user_name
        user_data = generate_random_user_data()
        # отправляем запрос на создание пользователя и проверяем полученные данные
        # user_token, refresh_token = create_user(user_data)
        create_and_check_user(user_data)

        # сохраняем полученные данные пользователя
        # self.user_data = user_data.copy()
        # self.to_teardown = True
        # добавляем полученные 2 токена в данные пользователя
        # self.user_data[KEYS.ACCESS_TOKEN] = user_token
        # self.user_data[KEYS.REFRESH_TOKEN] = refresh_token
        # _print_info(f'\nuser_data={self.user_data}\n')

