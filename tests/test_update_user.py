import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_create_user import HelpersOnCreateUser as u


class TestUpdateUser:

    @pytest.fixture
    @allure.title('Инициализируем данные пользователя для удаления после завершения работы')
    def __setup_user(self):
        # генерируем данные нового пользователя: email, password, user_name
        user_data = u.generate_random_user_data()
        # отправляем запрос на создание пользователя
        auth_token, refresh_token = u.create_user(user_data)
        # сохраняем полученные данные пользователя
        self.user_data = user_data.copy()
        self.auth_token = auth_token
        yield

        # Удаляем созданного пользователя
        u.try_to_delete_user(auth_token)


    @allure.title('Проверка обновления данных пользователя для авторизованного пользователя')
    @pytest.mark.parametrize('field', [         # обновляемое поле
        KEYS.PASSWORD_KEY,
        KEYS.NAME_KEY,
        KEYS.EMAIL_KEY,
    ])
    def test_update_user_success(self, __setup_user, field):
        # генерируем новые данные пользователя в поле field
        new_user_data = u.generate_random_user_data()
        # сохраняем новые данные пользователя с измененным полем field
        update_data = self.user_data.copy()
        update_data[field] = new_user_data[field]
        # формируем тело запроса для обновления поля field
        payload = {
            field: update_data[field]
        }
        # отправляем запрос на изменение данных пользователя
        response = u.try_to_update_user(payload, self.auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = c.check_success_ok(response)
        # проверяем полученные данные пользователя в теле ответа - поле "user"
        c.check_user_data(received_body, update_data)


    @allure.title('Проверка обновления данных пользователя для неавторизованного пользователя')
    @pytest.mark.parametrize('field', [         # обновляемое поле
        KEYS.PASSWORD_KEY,
        KEYS.NAME_KEY,
        KEYS.EMAIL_KEY,
    ])
    def test_update_user_not_authorized_error(self, __setup_user, field):
        # генерируем новые данные пользователя в поле field
        new_user_data = u.generate_random_user_data()
        # сохраняем новые данные пользователя с измененным полем field
        update_data = self.user_data.copy()
        update_data[field] = new_user_data[field]
        # формируем тело запроса для обновления поля field
        payload = {
            field: update_data[field]
        }
        # отправляем запрос на изменение данных пользователя без авторизации
        response = u.try_to_update_user(payload)

        # проверяем что получен код ответа 401
        # проверяем в теле ответа: { "success" = False }
        # проверяем сообщение в теле ответа: { "message" = "You should be authorised" }
        c.check_not_success_error_message(response, CODE.UNAUTHORIZED, message.UNAUTHORIZED)

