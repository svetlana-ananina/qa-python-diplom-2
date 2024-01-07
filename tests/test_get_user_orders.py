import pytest
import allure

from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from data import RESPONSE_MESSAGES as text

from helpers.helpers_on_check_response import check_ingredients, check_received_order_data, check_received_orders_list, \
    check_received_orders_info, check_success_ok, check_not_success_error_message
from helpers.helpers_on_check_response import _print_info
from helpers.helpers_on_create_user import  try_to_delete_user, create_user, create_order, try_to_get_user_orders
from helpers.helpers_on_get_ingredients import get_buns_list, get_fillings_list, get_sauces_list, get_ingredients


class TestGetUserOrders:

    ingredients = None
    buns_list = None
    fillings_list = None
    sauces_list = None

    @classmethod
    def setup_class(cls):
        """
        Инициализируем списки ингредиентов
        """
        _print_info(f'\nSetup_class "TestGetUserOrders" ...')
        # cls.ingredients = get_ingredients_from_api
        cls.ingredients = get_ingredients()
        cls.buns_list = get_buns_list(cls.ingredients)
        cls.fillings_list = get_fillings_list(cls.ingredients)
        cls.sauces_list = get_sauces_list(cls.ingredients)
        check_ingredients(cls.buns_list, cls.fillings_list, cls.sauces_list)

    def setup_method(self):
        """
        Инициализируем данные пользователя для удаления после завершения работы
        """
        _print_info(f'\nSetup_method "TestGetUserOrders" ...')
        # создаем пользователя
        auth_token, refresh_token = create_user()
        # Сохраняем данные для удаления созданного пользователя
        self._init_teardown(auth_token, refresh_token)

    def teardown_method(self):
        """
        Удаляем созданного пользователя
        """
        _print_info(f'\nTeardown_method "TestGetUserOrders" ...')
        _print_info(f'self.to_teardown={self.to_teardown}')
        if self.to_teardown:
            try_to_delete_user(self.auth_token)

    def _init_teardown(self, auth_token, refresh_token):
        """
        сохраняем полученные данные пользователя
        """
        self.to_teardown = True                 # Выполнять удаление созданного пользователя
        self.auth_token = auth_token
        self.refresh_token = refresh_token

    @classmethod
    def create_burger(cls):
        """
        Собираем бургер для заказа
        """
        ingredients_list = [
            (cls.buns_list[0])[KEYS.ID_KEY],
            (cls.fillings_list[0])[KEYS.ID_KEY],
            (cls.sauces_list[0])[KEYS.ID_KEY]
        ]
        _print_info(f'\ningredient_list={ingredients_list}')
        return ingredients_list

    @allure.title('Проверка получения заказов для авторизованного пользователя - 1 заказ')
    def test_get_user_orders_authorized_user(self):
        # получаем список ингредиентов и составляем заказ
        ingredients_list = self.create_burger()

        # отправляем запрос на создание заказа для пользователя
        order_number, order_name = create_order(ingredients_list, auth_token=self.auth_token)
        _print_info(f'\norder_number={order_number}')
        _print_info(f'order_name="{order_name}"')

        # отправляем запрос на получение заказов пользователя
        response = try_to_get_user_orders(self.auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = check_success_ok(response)

        # проверяем поле "orders"  и количество заказов, получаем список заказов
        received_orders_list = check_received_orders_list(received_body, 1)

        # проверяем полученные данные заказа
        received_order_data = received_orders_list[0]
        check_received_order_data(received_order_data, order_number, order_name, ingredients_list)

        # проверяем поля "total" и "totalToday" в теле ответа
        check_received_orders_info(received_body, 1)


    @allure.title('Проверка получения заказов для авторизованного пользователя - нет заказов')
    def test_get_user_orders_authorized_user_no_orders(self):
        # получаем заказы пользователя
        response = try_to_get_user_orders(self.auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = check_success_ok(response)

        # проверяем поле "orders" и количество заказов
        received_orders_list = check_received_orders_list(received_body, 0)

        # проверяем поля "total" и "totalToday" в теле ответа
        check_received_orders_info(received_body, 0)


    @allure.title('Проверка получения заказов для неавторизованного пользователя')
    def test_get_user_orders_unauthorized_user_error(self):
        # получаем заказы пользователя
        response = try_to_get_user_orders()

        # проверяем что получен код ответа 401
        # проверяем в теле ответа: { "success" = False }
        # проверяем сообщение в теле ответа: { "message" = "You should be authorised" }
        check_not_success_error_message(response, CODE.UNAUTHORIZED, text.UNAUTHORIZED)

