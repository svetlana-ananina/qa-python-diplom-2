import pytest
import allure

from data import StatusCodes as CODE
from data import ResponseKeys as KEYS
from data import ResponseMessages as message

from helpers.helpers_on_check_response import HelpersOnCheck as c
from helpers.helpers_on_create_user import HelpersOnCreateUser as u


class TestUpdateUser:

    @allure.title('Проверка обновления данных пользователя для авторизованного пользователя')
    @pytest.mark.parametrize('field', [         # обновляемое поле
        KEYS.EMAIL_KEY,
        KEYS.NAME_KEY,
        KEYS.PASSWORD_KEY,
    ])
    def test_update_user_success(self, setup_user, field):
        user_data, auth_token = setup_user
        # генерируем новые данные пользователя в поле field
        new_user_data = u.generate_random_user_data()
        # сохраняем новые данные пользователя с измененным полем field
        update_data = user_data.copy()
        update_data[field] = new_user_data[field]
        # формируем тело запроса для обновления поля field
        payload = {
            field: update_data[field]
        }
        # отправляем запрос на изменение данных пользователя
        response = u.try_to_update_user(payload, auth_token)

        # Проверяем, что получен статус-код 200 OK и в теле ответа "success" = True
        # и получаем тело ответа
        received_body = c.check_success_ok(response)
        # проверяем полученные данные пользователя в теле ответа - поле "user"
        c.check_user_data(received_body, update_data)


    @allure.title('Проверка обновления данных пользователя для неавторизованного пользователя')
    @pytest.mark.parametrize('field', [         # обновляемое поле
        KEYS.EMAIL_KEY,
        KEYS.NAME_KEY,
        KEYS.PASSWORD_KEY,
    ])
    def test_update_user_not_authorized_error(self, setup_user, field):
        user_data, auth_token = setup_user
        # генерируем новые данные пользователя в поле field
        new_user_data = u.generate_random_user_data()
        # сохраняем новые данные пользователя с измененным полем field
        update_data = user_data.copy()
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

