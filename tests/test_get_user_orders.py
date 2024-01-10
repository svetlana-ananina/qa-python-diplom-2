import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_create_user import HelpersOnCreateUser as u
from helpers.helpers_on_get_ingredients import HelpersOnGetIngredients as g


@pytest.fixture(scope='class')
@allure.title('Инициализируем списки ингредиентов')
def setup_ingredients():
    ingredients = g.get_ingredients()
    TestGetUserOrders.buns_list = g.get_buns_list(ingredients)
    TestGetUserOrders.fillings_list = g.get_fillings_list(ingredients)
    TestGetUserOrders.sauces_list = g.get_sauces_list(ingredients)
    c.check_ingredients(TestGetUserOrders.buns_list, TestGetUserOrders.fillings_list, TestGetUserOrders.sauces_list)


@pytest.mark.usefixtures('setup_ingredients', scope='class')
class TestGetUserOrders:

    buns_list = None
    fillings_list = None
    sauces_list = None


    @allure.step('Собираем бургер для заказа')
    def __create_burger(self):
        ingredients_list = [
            (self.buns_list[0])[KEYS.ID_KEY],
            (self.fillings_list[0])[KEYS.ID_KEY],
            (self.sauces_list[0])[KEYS.ID_KEY],
        ]
        return ingredients_list


    @allure.title('Проверка получения заказов для авторизованного пользователя - 1 заказ')
    def test_get_user_orders_authorized_user(self, setup_user):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # получаем список ингредиентов и составляем заказ
        ingredients_list = self.__create_burger()
        # отправляем запрос на создание заказа для пользователя
        order_number, order_name = u.create_order(ingredients_list, auth_token)
        # отправляем запрос на получение заказов пользователя
        response = u.try_to_get_user_orders(auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = c.check_success_ok(response)
        # проверяем поле "orders" и количество заказов, получаем список заказов
        received_orders_list = c.check_received_orders_list(received_body, 1)
        # проверяем полученные данные заказа
        received_order_data = received_orders_list[0]
        c.check_received_order_data(received_order_data, order_number, order_name, ingredients_list)
        # проверяем поля "total" и "totalToday" в теле ответа
        c.check_received_orders_info(received_body, 1)


    @allure.title('Проверка получения заказов для авторизованного пользователя - нет заказов')
    def test_get_user_orders_authorized_user_no_orders(self, setup_user):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        user_data, auth_token = setup_user
        # получаем заказы пользователя
        response = u.try_to_get_user_orders(auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = c.check_success_ok(response)
        # проверяем поле "orders" и количество заказов
        c.check_received_orders_list(received_body, 0)
        # проверяем поля "total" и "totalToday" в теле ответа
        c.check_received_orders_info(received_body, 0)


    @allure.title('Проверка получения заказов для неавторизованного пользователя')
    def test_get_user_orders_unauthorized_user_error(self):
        # получаем заказы пользователя
        response = u.try_to_get_user_orders()

        # проверяем что получен код ответа 401
        # проверяем в теле ответа: { "success" = False }
        # проверяем сообщение в теле ответа: { "message" = "You should be authorised" }
        c.check_not_success_error_message(response, CODE.UNAUTHORIZED, message.UNAUTHORIZED)

