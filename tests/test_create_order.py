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
    TestCreateOrder.buns_list = g.get_buns_list(ingredients)
    TestCreateOrder.fillings_list = g.get_fillings_list(ingredients)
    TestCreateOrder.sauces_list = g.get_sauces_list(ingredients)
    c.check_ingredients(TestCreateOrder.buns_list, TestCreateOrder.fillings_list, TestCreateOrder.sauces_list)


@pytest.fixture
@allure.title('Инициализируем данные пользователя для удаления после завершения работы')
def setup_user():
    # генерируем данные нового пользователя: email, password, user_name
    user_data = u.generate_random_user_data()
    # отправляем запрос на создание пользователя
    auth_token, refresh_token = u.create_user(user_data)
    # сохраняем полученные данные пользователя
    yield auth_token

    # Удаляем созданного пользователя
    u.try_to_delete_user(auth_token)


@pytest.mark.usefixtures('setup_ingredients', scope='class')
class TestCreateOrder:

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


    @allure.title('Проверка создания заказа для авторизованного пользователя')
    def test_create_order_authorized_user(self, setup_user):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        auth_token = setup_user
        # составляем список ингредиентов для бургера
        ingredients_id_list = self.__create_burger()
        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list, auth_token)

        # проверяем полученный ответ и данные заказа
        c.check_order_data(response)


    @allure.title('Проверка создания заказа для авторизованного пользователя')
    def test_create_order_two_orders_for_authorized_user(self, setup_user):
        # сохраняем авторизационный токен пользователя, полученный при регистрации
        auth_token = setup_user
        # составляем список ингредиентов для бургера
        ingredients_id_list = self.__create_burger()
        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list, auth_token)
        # проверяем полученный ответ и данные заказа
        c.check_order_data(response)
        # отправляем запрос на создание еще одного заказа
        response = u.try_to_create_order(ingredients_id_list, auth_token)

        # проверяем полученный ответ и данные заказа
        c.check_order_data(response)


    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_unauthorized(self):
        # составляем список ингредиентов для бургера
        ingredients_id_list = self.__create_burger()
        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list)

        # проверяем полученный ответ и данные заказа
        c.check_order_data(response)


    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_no_ingredients(self):
        # составляем список ингредиентов для бургера
        ingredients_id_list = []
        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list)

        # проверяем что получен код ответа 400
        # проверяем в теле ответа: { "success" = False }
        # проверяем сообщение в теле ответа: { "message" = "You should be authorised" }
        c.check_not_success_error_message(response, CODE.BAD_REQUEST, message.NO_INGREDIENTS)


    @allure.title('Проверка создания заказа с неверным хешем ингредиента')
    def test_create_order_invalid_ingredient_hash(self):
        # составляем список ингредиентов для бургера
        ingredients_id_list = ['0000000000']
        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list)

        # проверяем что получен код ответа 500
        c.check_status_code(response, CODE.ERROR_500)


