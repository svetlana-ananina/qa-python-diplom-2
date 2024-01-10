import allure

from data import StatusCodes as CODE, ResponseKeys as KEYS, Endpoints as e


#
# Вспомогательные методы проверки ответа на запрос к API
class HelpersOnCheck:

    @staticmethod
    @allure.step('Проверяем наличие ключа в ответе')
    def check_key_in_body(response_body, key):
        # проверяем что в ответе есть ключ key
        assert key in response_body, f'В ответе отсутствует ключ "{key}", получен ответ: "{response_body}"'
        return response_body[key]

    @staticmethod
    @allure.step('Проверяем значение ключа в ответе')
    def check_key_and_value_in_body(response_body, key, value):
        # проверяем наличие ключа в ответе
        assert key in response_body, f'В ответе отсутствует ключ "{key}", получен ответ: "{response_body}"'
        # проверяем значение ключа в ответе
        received_value = response_body[key]
        assert received_value == value, f'Получено неверное значение ключа "{key}": ожидалось "{value}", получено "{received_value}"'
        return received_value

    @staticmethod
    @allure.step('Проверяем код ответа')
    def check_status_code(response, expected_code):
        # проверяем что получен код ответа expected_code
        received_code = response.status_code
        assert received_code == expected_code, f'Неверный код в ответе: ожидался {expected_code}, получен "{received_code}", ответ: "{response.text}"'

    @staticmethod
    @allure.step('Проверяем значение поля "success" в ответе')
    def check_success(response, expected_value):
        received_text = response.text
        # проверяем что в ответе есть "success"
        assert KEYS.SUCCESS_KEY in response.json(), f'В ответе отсутствует ключ "{KEYS.SUCCESS_KEY}", получено: "{received_text}"'
        # проверяем тело ответа
        received_body = response.json()
        # проверяем сообщение об ошибке
        received_value = received_body[KEYS.SUCCESS_KEY]
        assert received_value == expected_value, f'Получено неверное значение поля "{KEYS.SUCCESS_KEY}": ожидалось "{expected_value}", получено "{received_value}"'
        return received_body

    @staticmethod
    @allure.step('Проверяем, что запрос выполнен успешно')
    def check_success_ok(response):
        # проверяем что получен код ответа 200
        HelpersOnCheck.check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        return HelpersOnCheck.check_success(response, True)

    @staticmethod
    @allure.step('Проверяем код ошибки и сообщение об ошибке')
    def check_not_success_error_message(response, code, message):
        # проверяем что получен код ответа = code
        HelpersOnCheck.check_status_code(response, code)
        # проверяем в теле ответа: { "success" = False }
        received_body = HelpersOnCheck.check_success(response, False)
        # проверяем сообщение в теле ответа: { "message" = message }
        HelpersOnCheck.check_message(received_body, message)
        return received_body

    @staticmethod
    @allure.step('Проверяем сообщение в ответе')
    def check_message(received_body, expected_message):
        # проверяем что в ответе есть "message"
        assert KEYS.MESSAGE_KEY in received_body, f'В ответе отсутствует ключ "{KEYS.MESSAGE_KEY}", получено: "{received_body}"'
        # проверяем сообщение об ошибке
        received_message = received_body[KEYS.MESSAGE_KEY]
        assert received_message == expected_message, f'Получено неверное значение поля "{KEYS.MESSAGE_KEY}":\nожидалось "{expected_message}"\nполучено "{received_message}"'
        return received_message

    @staticmethod
    @allure.step('Получаем значение ключа')
    def get_key_from_body(response_body, key):
        return response_body[key]

    #
    # Проверка полученных данных пользователя после создания/авторизации пользователя
    @staticmethod
    @allure.step('Проверяем полученные данные пользователя - поле "user"')
    def check_user_data(received_body, user_data):
        # проверяем наличие в ответе ключа "user" и получаем его значение - словарь
        received_user_data = HelpersOnCheck.check_key_in_body(received_body, KEYS.USER_KEY)
        assert type(received_user_data) is dict

        # проверяем в словаре "user" наличие и значения полей "email" и "name"
        email = user_data[KEYS.EMAIL_KEY]
        name = user_data[KEYS.NAME_KEY]
        HelpersOnCheck.check_key_and_value_in_body(received_user_data, KEYS.EMAIL_KEY, email)
        HelpersOnCheck.check_key_and_value_in_body(received_user_data, KEYS.NAME_KEY, name)

    @staticmethod
    @allure.step('Проверяем полученные данные пользователя после регистрации/авторизации')
    def check_new_user_data(received_body, user_data):
        # проверяем наличие в ответе ключа "user" и значения полей "email" и "name"
        HelpersOnCheck.check_user_data(received_body, user_data)

        # проверяем наличие в ответе ключа "accessToken" и получаем его значение - строку "Bearer ..."
        auth_token = HelpersOnCheck.check_key_in_body(received_body, KEYS.ACCESS_TOKEN)
        # проверяем формат токена: "Bearer ..."
        assert (type(auth_token) is str and
                e.ACCESS_TOKEN_PREFIX in auth_token and
                len(auth_token) > len(
                    e.ACCESS_TOKEN_PREFIX)), f'Получено неверное значение ключа "{KEYS.ACCESS_TOKEN}": неправильный формат "{KEYS.ACCESS_TOKEN}"={auth_token}'

        # проверяем наличие в ответе ключа "refreshToken" и получаем его значение - строку `"..."
        refresh_token = HelpersOnCheck.check_key_in_body(received_body, KEYS.REFRESH_TOKEN)
        # проверяем токен
        assert (type(refresh_token) is str and
                len(refresh_token) > 0), f'Получено неверное значение ключа "{KEYS.REFRESH_TOKEN}": неправильный формат "{KEYS.REFRESH_TOKEN}"={refresh_token}'
        # возвращаем полученные токены
        return auth_token, refresh_token

    #
    # Проверка полученных данных после создания заказа
    @staticmethod
    @allure.step('Проверяем полученный ответ после запроса создания заказа')
    # def check_order_data(received_body):
    def check_order_data(response):
        # проверяем что получен код ответа 200
        HelpersOnCheck.check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = HelpersOnCheck.check_success(response, True)
        # проверяем полученные данные заказа в теле ответа

        # проверяем наличие в ответе ключа "name" и получаем его значение - строка
        order_name = HelpersOnCheck.check_key_in_body(received_body, KEYS.NAME_KEY)
        assert type(order_name) is str, f'Получено неверное значение ключа "{KEYS.NAME_KEY}": ожидалось - строка, получено значение {order_name} тип {type(order_name)}'

        # проверяем наличие в ответе ключа "order" и получаем его значение - словарь
        received_order_data = HelpersOnCheck.check_key_in_body(received_body, KEYS.ORDER_KEY)
        assert type(received_order_data) is dict

        # проверяем в словаре "order" наличие и значения поля "number"
        order_number = HelpersOnCheck.check_key_in_body(received_order_data, KEYS.NUMBER_KEY)
        assert str(
            order_number).isdigit(), f'Получено неверное значение ключа "{KEYS.NUMBER_KEY}": ожидалось - число, получено значение {order_number} тип {type(order_number)}'

        return order_number, order_name

    @staticmethod
    @allure.step('Проверяем списки ингредиентов по типам - булки, начинки, соусы')
    def check_ingredients(buns_list, fillings_list, sauces_list):
        assert len(buns_list) != 0 and len(fillings_list) != 0 and len(sauces_list) != 0, \
            f'TestCreateOrder ошибка - в списке ингредиентов нет по крайней мере одного из необходимых типов (булки, начинки, соусы)'

    @staticmethod
    @allure.step('Проверяем полученный ответ на запрос списка ингредиентов')
    def check_ingredients_list(response):
        # проверяем что получен код ответа 200
        HelpersOnCheck.check_status_code(response, CODE.OK)
        # проверяем в теле ответа: { "success" = True }
        received_body = HelpersOnCheck.check_success(response, True)
        # проверяем наличие в ответе ключа "data" и получаем его значение - список ингредиентов (словарь)
        ingredients = HelpersOnCheck.check_key_in_body(received_body, KEYS.DATA)
        # проверяем что поле data содержит список и возвращаем его
        assert type(ingredients) is list and len(ingredients) > 0
        return ingredients

    #
    # Проверка полученного ответа на запрос получения заказов пользователя
    @staticmethod
    @allure.step('Проверяем в полученном ответе информацию о заказе')
    def check_received_order_data(received_order_data, order_number, order_name, ingredients_list):
        # проверяем полученные данные заказа
        assert type(received_order_data) is dict
        # проверяем что поле "_id" строка
        received_order_id = HelpersOnCheck.check_key_in_body(received_order_data, KEYS.ID_KEY)
        assert type(received_order_id) is str
        # проверяем что поле "number" = order_number
        HelpersOnCheck.check_key_and_value_in_body(received_order_data, KEYS.NUMBER_KEY, order_number)
        # проверяем что поле "name" = order_name
        HelpersOnCheck.check_key_and_value_in_body(received_order_data, KEYS.NAME_KEY, order_name)
        # проверяем поле "ingredients"
        received_ingredients_list = HelpersOnCheck.check_key_in_body(received_order_data, KEYS.INGREDIENTS)
        assert type(received_ingredients_list) is list
        # проверяем что количество ингредиентов совпадает с заданным
        assert len(received_ingredients_list) == len(ingredients_list)

    @staticmethod
    @allure.step('Проверяем в полученном ответе поле "orders" - список заказов')
    def check_received_orders_list(received_body, amount):
        # проверяем наличие в ответе ключа "orders" и получаем его значение - список
        received_orders_list = HelpersOnCheck.check_key_in_body(received_body, KEYS.ORDERS_KEY)
        assert type(received_orders_list) is list
        # проверяем что количество заказов в списке = amount
        assert len(received_orders_list) == amount
        return received_orders_list

    @staticmethod
    @allure.step('Проверяем в полученном ответе поля "total" и "totalToday"')
    def check_received_orders_info(received_body, amount):
        # проверяем поля "total" и "totalToday" в списке заказов "orders" (в теле ответа)
        HelpersOnCheck.check_key_and_value_in_body(received_body, KEYS.TOTAL_KEY, amount)
        HelpersOnCheck.check_key_and_value_in_body(received_body, KEYS.TOTAL_TODAY_KEY, amount)

