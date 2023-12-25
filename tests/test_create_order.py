import pytest
import allure

from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from data import RESPONSE_MESSAGES as text

from helpers.helpers_on_check_response import check_status_code, check_success, check_user_data, check_message, \
    check_order_data
from helpers.helpers_on_check_response import _print_info
from helpers.helpers_on_create_user import generate_random_user_data, try_to_delete_user, create_user, \
    get_ingredients, try_to_create_order, get_buns_list, get_fillings_list, get_sauces_list


class TestCreateOrder:

    def setup(self):
        """
        Инициализируем данные пользователя для удаления после завершения работы
        """
        _print_info(f'\nSetup "TestCreateOrder" ...')
        # Получаем список ингредиентов
        ingredients = get_ingredients()
        #_print_info(f'ingredients = {ingredients}')
        # получаем списки булок, начинок и соусов
        self.buns_list = get_buns_list(ingredients)
        self.fillings_list = get_fillings_list(ingredients)
        self.sauces_list = get_sauces_list(ingredients)
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
        user_data = generate_random_user_data()
        # отправляем запрос на создание пользователя
        auth_token, refresh_token = create_user(user_data)
        # сохраняем полученные данные пользователя
        self.init_teardown(auth_token, refresh_token)

        assert len(self.buns_list) != 0 and len(self.fillings_list) != 0 and len(self.sauces_list) != 0, \
            f'TestCreateOrder ошибка - в списке ингредиентов нет по крайней мере одного из типов (булки, начинки, соусы)'
        # составляем список ингредиентов для бургера
        ingredients_id_list = [
            (self.buns_list[0])[KEYS.ID_KEY],
            (self.fillings_list[0])[KEYS.ID_KEY],
            (self.sauces_list[0])[KEYS.ID_KEY]
        ]
        _print_info(f'ingredients_id_list={ingredients_id_list}')

        # отправляем запрос на создание заказа
        response = try_to_create_order(ingredients_id_list, auth_token)

        # проверяем что получен код ответа 200
        check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = check_success(response, True)
        # проверяем полученные данные пользователя в теле ответа - поле "user"
        order_number, order_name = check_order_data(received_body)
        _print_info(f'order_number={order_number}')
        _print_info(f'order_name="{order_name}"')

