import pytest
import allure

from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from data import RESPONSE_MESSAGES as text

from helpers.helpers_on_check_response import check_status_code, check_success, check_user_data, check_message
from helpers.helpers_on_check_response import _print_info
from helpers.helpers_on_create_user import generate_random_user_data, try_to_delete_user, create_user, \
    try_to_update_user, generate_random_user_name, generate_random_user_login, generate_random_user_password, \
    get_ingredients, try_to_create_order, get_ingredients_by_type


class TestCreateOrder:

    def setup(self):
        """
        Инициализируем данные пользователя для удаления после завершения работы
        """
        _print_info(f'\nSetup "TestCreateOrder" ...')
        # Получаем список ингредиентов
        self.ingredient_list = get_ingredients()
        _print_info(f'self.ingredient_list = {self.ingredient_list}')
        # получаем списки булок, начинок и соусов
        self.bun_list, self.fillings_list, self.sauce_list = get_ingredients_by_type(self.ingredient_list)
        _print_info(f'self.bun_list = {self.bun_list}')
        _print_info(f'self.fillings_list = {self.fillings_list}')
        _print_info(f'self.sauce_list = {self.sauce_list}')
        self.to_teardown = False        # Выполнять удаление созданного пользователя
        self.auth_token = None
        self.refresh_token = None
        self.ingredients = None

    def teardown(self):
        """
        Удаляем созданного пользователя
        """
        _print_info(f'\nTeardown "TestCreateOrder" ...')
        _print_info(f'self.to_teardown={self.to_teardown}')
        if self.to_teardown:
            try_to_delete_user(self.auth_token)

    def init_teardown(self, auth_token, refresh_token):
        # сохраняем полученные данные пользователя
        self.to_teardown = True
        self.auth_token = auth_token
        self.refresh_token = refresh_token

    @allure.title('Проверка обновления данных пользователя для авторизованного пользователя')
    def test_create_order(self):
        # генерируем данные пользователя: email, password, user_name
        # user_data = generate_random_user_data()
        # отправляем запрос на создание пользователя
        # auth_token, refresh_token = create_user(user_data)
        # сохраняем полученные данные пользователя
        # self.init_teardown(auth_token, refresh_token)

        assert len(self.bun_list) != 0 and len(self.fillings_list) != 0 and len(self.sauce_list) != 0, \
            f'TestCreateOrder ошибка - в списке ингредиентов нет по крайней мере одного из типов (булки, начинки, соусы)'
        # составляем список ингредиентов для бургера
        ingredients_id = [
            (self.bun_list[0])[KEYS.ID_KEY],
            (self.fillings_list[0])[KEYS.ID_KEY],
            (self.sauce_list[0])[KEYS.ID_KEY]
        ]
        res = try_to_create_order(ingredients_id)


