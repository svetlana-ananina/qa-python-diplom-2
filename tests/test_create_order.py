import pytest
import allure

from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from data import RESPONSE_MESSAGES as text

from helpers.helpers_on_check_response import check_status_code, check_success, check_user_data, check_message, \
    check_order_data, check_ingredients, check_not_success_error_message
from helpers.helpers_on_check_response import _print_info
from helpers.helpers_on_create_user import generate_random_user_data, try_to_delete_user, create_user, try_to_create_order
from helpers.helpers_on_get_ingredients import create_ingredient_list_for_burger, get_ingredients, get_buns_list, \
    get_fillings_list, get_sauces_list


class TestCreateOrder:

    ingredients = None
    buns_list = None
    fillings_list = None
    sauces_list = None

    @classmethod
    def setup_class(cls):
        """
        Инициализируем списки ингредиентов
        """
        _print_info(f'\nSetup_class "TestCreateOrder" ...')
        # cls.ingredients = get_ingredients_from_api
        cls.ingredients = get_ingredients()
        cls.buns_list = get_buns_list(cls.ingredients)
        cls.fillings_list = get_fillings_list(cls.ingredients)
        cls.sauces_list = get_sauces_list(cls.ingredients)
        check_ingredients(cls.buns_list, cls.fillings_list, cls.sauces_list)

    def setup(self):
        """
        Инициализируем данные пользователя для удаления после завершения работы
        """
        _print_info(f'\nSetup "TestCreateOrder" ...')
        self.to_teardown = False
        self.auth_token = None
        self.refresh_token = None

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

    @allure.title('Проверка создания заказа для авторизованного пользователя')
    def test_create_order_authorized_user(self):
        # отправляем запрос на создание пользователя
        auth_token, refresh_token = create_user()
        # сохраняем полученные данные пользователя
        self.init_teardown(auth_token, refresh_token)
        # составляем список ингредиентов для бургера
        #ingredients_id_list = create_ingredient_list_for_burger(self.buns_list, self.fillings_list, self.sauces_list)
        ingredients_id_list = self.create_burger()
        _print_info(f'ingredients_id_list={ingredients_id_list}')

        # отправляем запрос на создание заказа
        response = try_to_create_order(ingredients_id_list, auth_token)

        # проверяем полученный ответ и данные заказа
        order_number, order_name = check_order_data(response)
        _print_info(f'order_number={order_number}')
        _print_info(f'order_name="{order_name}"')


    @allure.title('Проверка создания заказа для авторизованного пользователя')
    def test_create_order_two_orders_for_authorized_user(self):
        # отправляем запрос на создание пользователя
        auth_token, refresh_token = create_user()
        # сохраняем полученные данные пользователя
        self.init_teardown(auth_token, refresh_token)
        # составляем список ингредиентов для бургера
        #ingredients_id_list = create_ingredient_list_for_burger(self.buns_list, self.fillings_list, self.sauces_list)
        ingredients_id_list = self.create_burger()
        _print_info(f'ingredients_id_list={ingredients_id_list}')

        # отправляем запрос на создание заказа
        response = try_to_create_order(ingredients_id_list, auth_token)
        # проверяем полученный ответ и данные заказа
        order_number, order_name = check_order_data(response)

        # отправляем запрос на создание еще одного заказа
        response = try_to_create_order(ingredients_id_list, auth_token)
        # проверяем полученный ответ и данные заказа
        order_number, order_name = check_order_data(response)


    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_unauthorized(self):
        # составляем список ингредиентов для бургера
        #ingredients_id_list = create_ingredient_list_for_burger(self.buns_list, self.fillings_list, self.sauces_list)
        ingredients_id_list = self.create_burger()
        _print_info(f'ingredients_id_list={ingredients_id_list}')

        # отправляем запрос на создание заказа
        response = try_to_create_order(ingredients_id_list)

       # проверяем полученный ответ и данные заказа
        order_number, order_name = check_order_data(response)
        _print_info(f'order_number={order_number}')
        _print_info(f'order_name="{order_name}"')

    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_no_ingredients(self):
        # составляем список ингредиентов для бургера
        ingredients_id_list = []
        _print_info(f'ingredients_id_list={ingredients_id_list}')

        # отправляем запрос на создание заказа
        response = try_to_create_order(ingredients_id_list)

        # проверяем что получен код ответа 400
        # проверяем в теле ответа: { "success" = False }
        # проверяем сообщение в теле ответа: { "message" = "You should be authorised" }
        check_not_success_error_message(response, CODE.BAD_REQUEST, text.NO_INGREDIENTS)



    @allure.title('Проверка создания заказа с неверным хешем ингредиента')
    def test_create_order_invalid_ingredient_hash(self):
        # составляем список ингредиентов для бургера
        ingredients_id_list = ['0000000000']
        _print_info(f'ingredients_id_list={ingredients_id_list}')

        # отправляем запрос на создание заказа
        response = try_to_create_order(ingredients_id_list)

        # проверяем что получен код ответа 500
        check_status_code(response, CODE.ERROR_500)


