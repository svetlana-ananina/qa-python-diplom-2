import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_create_user import HelpersOnCreateUser as u
from helpers.helpers_on_get_ingredients import HelpersOnGetIngredients as g


def _print_info(info):
    print(info)


@pytest.fixture()
@allure.title('Инициализируем списки ингредиентов')
def setup_ingredients():
    _print_info(f'\nsetup_ingredients "TestCreateOrder" ...')
    ingredients = g.get_ingredients()
    buns_list = g.get_buns_list(ingredients)
    fillings_list = g.get_fillings_list(ingredients)
    sauces_list = g.get_sauces_list(ingredients)
    c.check_ingredients(buns_list, fillings_list, sauces_list)
    TestCreateOrder.buns_list = buns_list
    TestCreateOrder.fillings_list = fillings_list
    TestCreateOrder.sauces_list = sauces_list


@pytest.mark.usefixtures('setup_ingredients', scope='class')
class TestCreateOrder:

    #ingredients = None
    buns_list = None
    fillings_list = None
    sauces_list = None


    """
    @classmethod
    @pytest.fixture()
    @allure.title('Инициализируем списки ингредиентов')
    def setup_ingredients(cls):
        _print_info(f'\nsetup_ingredients "TestCreateOrder" ...')
        cls.ingredients = g.get_ingredients()
        cls.buns_list = g.get_buns_list(cls.ingredients)
        cls.fillings_list = g.get_fillings_list(cls.ingredients)
        cls.sauces_list = g.get_sauces_list(cls.ingredients)
        c.check_ingredients(cls.buns_list, cls.fillings_list, cls.sauces_list)
    """

    @pytest.fixture
    @allure.title('Инициализируем данные пользователя для удаления после завершения работы')
    def __setup_user(self):
        # генерируем данные нового пользователя: email, password, user_name
        user_data = u.generate_random_user_data()
        # отправляем запрос на создание пользователя
        auth_token, refresh_token = u.create_user(user_data)
        # сохраняем полученные данные пользователя
        self.auth_token = auth_token
        yield

        # Удаляем созданного пользователя
        u.try_to_delete_user(auth_token)


    @allure.step('Собираем бургер для заказа')
    def __create_burger(self):
        ingredients_list = [
            (self.buns_list[0])[KEYS.ID_KEY],
            (self.fillings_list[0])[KEYS.ID_KEY],
            (self.sauces_list[0])[KEYS.ID_KEY],
        ]
        _print_info(f'\ningredient_list={ingredients_list}')
        return ingredients_list


    @allure.title('Проверка создания заказа для авторизованного пользователя')
    def test_create_order_authorized_user(self, __setup_user):
        # составляем список ингредиентов для бургера
        ingredients_id_list = self.__create_burger()
        _print_info(f'ingredients_id_list={ingredients_id_list}')

        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list, self.auth_token)

        # проверяем полученный ответ и данные заказа
        order_number, order_name = c.check_order_data(response)
        _print_info(f'order_number={order_number}')
        _print_info(f'order_name="{order_name}"')


    @allure.title('Проверка создания заказа для авторизованного пользователя')
    def test_create_order_two_orders_for_authorized_user(self, __setup_user):
        # составляем список ингредиентов для бургера
        ingredients_id_list = self.__create_burger()
        _print_info(f'ingredients_id_list={ingredients_id_list}')

        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list, self.auth_token)
        # проверяем полученный ответ и данные заказа
        order_number, order_name = c.check_order_data(response)

        # отправляем запрос на создание еще одного заказа
        response = u.try_to_create_order(ingredients_id_list, self.auth_token)
        # проверяем полученный ответ и данные заказа
        order_number, order_name = c.check_order_data(response)


    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_unauthorized(self):
        # составляем список ингредиентов для бургера
        ingredients_id_list = self.__create_burger()
        _print_info(f'ingredients_id_list={ingredients_id_list}')

        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list)

        # проверяем полученный ответ и данные заказа
        order_number, order_name = c.check_order_data(response)
        _print_info(f'order_number={order_number}')
        _print_info(f'order_name="{order_name}"')


    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_no_ingredients(self):
        # составляем список ингредиентов для бургера
        ingredients_id_list = []
        _print_info(f'ingredients_id_list={ingredients_id_list}')

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
        _print_info(f'ingredients_id_list={ingredients_id_list}')

        # отправляем запрос на создание заказа
        response = u.try_to_create_order(ingredients_id_list)

        # проверяем что получен код ответа 500
        c.check_status_code(response, CODE.ERROR_500)


