import pytest
import allure

from conftest import get_ingredients_from_api, get_buns_list_from_api, get_fillings_list_from_api, get_sauces_list_from_api
from data import STATUS_CODES as CODE
from data import RESPONSE_KEYS as KEYS
from data import RESPONSE_MESSAGES as text

from helpers.helpers_on_check_response import check_status_code, check_success, check_user_data, check_message, \
    check_order_data, check_ingredients, check_key_in_body, check_key_and_value_in_body, _print_response_value
from helpers.helpers_on_check_response import _print_info
from helpers.helpers_on_create_user import generate_random_user_data, try_to_delete_user, create_user, \
    create_order, try_to_get_user_orders
from helpers.helpers_on_get_ingredients import create_ingredient_list_for_burger, get_buns_list, get_fillings_list, \
    get_sauces_list
from helpers.ingredients_list import MyIngredientsList


@pytest.mark.usefixtures('get_ingredients_from_api')
@pytest.mark.usefixtures('get_buns_list_from_api')
@pytest.mark.usefixtures('get_fillings_list_from_api')
@pytest.mark.usefixtures('get_sauces_list_from_api')
class TestGetUserOrders:
    #ingredients = get_ingredients_from_api
    ingredients = MyIngredientsList()

    def setup(self):
        """
        Инициализируем данные пользователя для удаления после завершения работы
        """
        _print_info(f'\nSetup "TestGetUserOrders" ...')
        # Получаем список ингредиентов
        #ingredients = get_ingredients_from_api

        #self.buns_list, self.fillings_list, self.sauces_list = get_ingredients_from_api
        #self.buns_list = get_buns_list_from_api
        #self.fillings_list = get_fillings_list_from_api
        #self.sauces_list = get_sauces_list_from_api
        #self._init_buns_list()
        #self._init_fillings_list()
        #self._init_sauces_list_()


        # создаем пользователя
        auth_token, refresh_token = create_user()
        # Сохраняем данные для удаления созданного пользователя
        self._init_teardown(auth_token, refresh_token)

    #@pytest.mark.usefixtures('get_ingredients_from_api')
    #def _init_ingredients(self):
    #    self.ingredients = get_ingredients_from_api.copy()

    #@pytest.mark.usefixtures('get_ingredients_from_api')
    #@pytest.mark.usefixtures('get_buns_list_from_api')
    #def _init_buns_list(self):
    #    self.buns_list = get_buns_list_from_api

    #@pytest.mark.usefixtures('get_ingredients_from_api')
    #@pytest.mark.usefixtures('get_fillings_list_from_api')
    #def _init_fillings_list(self):
    #    self.fillings_list = get_fillings_list_from_api

    #@pytest.mark.usefixtures('get_ingredients_from_api')
    #@pytest.mark.usefixtures('get_sauces_list_from_api')
    #def _init_sauces_list_(self):
    #    self.sauces_list = get_sauces_list_from_api

    def teardown(self):
        """
        Удаляем созданного пользователя
        """
        _print_info(f'\nTeardown "TestGetUserOrders" ...')
        _print_info(f'self.to_teardown={self.to_teardown}')
        if self.to_teardown:
            try_to_delete_user(self.auth_token)

    def _init_teardown(self, auth_token, refresh_token):
        # сохраняем полученные данные пользователя
        self.to_teardown = True                 # Выполнять удаление созданного пользователя
        self.auth_token = auth_token
        self.refresh_token = refresh_token

    def _create_burger(self, buns_list, fillings_list, sauces_list):
        _print_response_value('buns_list', buns_list)
        _print_response_value('fillings_list', fillings_list)
        _print_response_value('sauces_list', sauces_list)
        _print_response_value('len(buns_list)', len(buns_list))
        _print_response_value('len(fillings_list)', len(fillings_list))
        _print_response_value('len(sauces_list)', len(sauces_list))
        _print_response_value('buns_list[0]', buns_list[0])
        _print_response_value('fillings_list[0]', fillings_list[0])
        _print_response_value('sauces_list[0]', sauces_list[0])
        ingredients_list = [
            (buns_list[0])[KEYS.ID_KEY],
            (fillings_list[0])[KEYS.ID_KEY],
            (sauces_list[0])[KEYS.ID_KEY]
        ]
        _print_info(f'ingredient_list={ingredients_list}')
        return ingredients_list

    @allure.title('Проверка получения заказов для авторизованного пользователя')
    def test_get_user_orders_authorized_user(self):
        # получаем список ингредиентов и составляем заказ
        #ingredient_list = create_ingredient_list_for_burger(self.buns_list, self.fillings_list, self.sauces_list)
        #ingredients_list = self._create_burger(self.buns_list, self.fillings_list, self.sauces_list)
        ingredients_list = self._create_burger(self.ingredients.get_buns_list(),
                                               self.ingredients.get_fillings_list(),
                                               self.ingredients.get_sauces_list())
        # отправляем запрос на создание заказа для пользователя
        order_number, order_name = create_order(ingredients_list, auth_token=self.auth_token)
        _print_info(f'\norder_number={order_number}')
        _print_info(f'order_name="{order_name}"')

        # получаем заказы пользователя
        response = try_to_get_user_orders(self.auth_token)

        # проверяем что получен код ответа 200
        check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = check_success(response, True)

        # проверяем наличие в ответе ключа "orders" и получаем его значение - список
        received_orders_list = check_key_in_body(received_body, KEYS.ORDERS_KEY)
        assert type(received_orders_list) is list
        # проверяем что количество заказов в списке = 1
        assert len(received_orders_list) == 1

        # проверяем полученные данные заказа
        received_order_data = received_orders_list[0]
        assert type(received_order_data) is dict
        # проверяем что поле "_id" строка
        received_order_id = check_key_in_body(received_order_data, KEYS.ID_KEY)
        assert type(received_order_id) is str
        # проверяем что поле "number" = order_number
        received_order_number = check_key_and_value_in_body(received_order_data, KEYS.NUMBER_KEY, order_number)
        # проверяем что поле "name" = order_name
        received_order_number = check_key_and_value_in_body(received_order_data, KEYS.NAME_KEY, order_name)
        # проверяем поле "ingredients"
        received_ingredients_list = check_key_in_body(received_order_data, KEYS.INGREDIENTS)
        assert type(received_ingredients_list) is list
        # проверяем что количество ингредиентов совпадает с заданным
        assert len(received_ingredients_list) == len(ingredients_list)

        # проверяем поля "total" и "totalToday" в списке заказов "orders" (в теле ответа)
        check_key_and_value_in_body(received_body, KEYS.TOTAL_KEY, 1)
        check_key_and_value_in_body(received_body, KEYS.TOTAL_TODAY_KEY, 1)


    @allure.title('Проверка получения заказов для авторизованного пользователя - нет заказов')
    def test_get_user_orders_authorized_user_no_orders(self):
        # получаем заказы пользователя
        response = try_to_get_user_orders(self.auth_token)

        # проверяем что получен код ответа 200
        check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = check_success(response, True)


