import pytest
import allure

from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from data import RESPONSE_MESSAGES as text

from helpers.helpers_on_check_response import check_status_code, check_success, check_user_data, check_message, \
    check_order_data, check_ingredients
from helpers.helpers_on_check_response import _print_info
from helpers.helpers_on_create_user import generate_random_user_data, try_to_delete_user, create_user, \
    get_ingredients, try_to_create_order, get_buns_list, get_fillings_list, get_sauces_list,  \
    create_ingredient_list_for_burger, get_ingredient_list, create_order


class TestGetUserOrders:

    def setup(self):
        """
        Инициализируем данные пользователя для удаления после завершения работы
        """
        _print_info(f'\nSetup "TestGetUserOrders" ...')
        # Получаем список ингредиентов
        #self.buns_list, self.fillings_list, self.sauces_list = get_ingredient_list()
        # создаем пользователя
        auth_token, refresh_token = create_user()
        # Сохраняем данные для удаления созданного пользователя
        self.init_teardown(auth_token, refresh_token)
        # отправляем запрос на создание заказа для пользователя
        received_body = create_order(auth_token=auth_token)
        # проверяем полученные данные заказа в теле ответа
        #order_number, order_name = check_order_data(received_body)
        #_print_info(f'order_number={order_number}')
        #_print_info(f'order_name="{order_name}"')

    def teardown(self):
        """
        Удаляем созданного пользователя
        """
        _print_info(f'\nTeardown "TestGetUserOrders" ...')
        _print_info(f'self.to_teardown={self.to_teardown}')
        if self.to_teardown:
            try_to_delete_user(self.auth_token)

    def init_teardown(self, auth_token, refresh_token):
        # сохраняем полученные данные пользователя
        self.to_teardown = True                 # Выполнять удаление созданного пользователя
        self.auth_token = auth_token
        self.refresh_token = refresh_token

    @allure.title('Проверка получения заказов для авторизованного пользователя')
    def test_get_user_orders_authorized_user(self):
        pass

