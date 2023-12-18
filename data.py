_to_print = True
# _to_print = False

# URL-адрес сервера
SERVER_URL = 'https://stellarburgers.nomoreparties.site'

# Эндпойнты (ручки) запросов к API
CREATE_USER = '/api/auth/register'  # Регистрация пользователя: POST '/api/auth/register'
LOGIN_USER = '/api/auth/login'  # Авторизация пользователя: POST '/api/auth/login'
LOGOUT_USER = '/api/auth/logout'  # Выход из системы: POST '/api/auth/logout'

DELETE_USER = '/api/auth/user'  # Удаление пользователя: DELETE '/api/auth/user'
GET_USER_DATA = '/api/auth/user'  # Получение данных пользователя: GET '/api/auth/user'
UPDATE_USER_DATA = '/api/auth/user'  # Обновление данных пользователя: PATCH '/api/auth/user'

UPDATE_TOKEN = '/api/auth/token'  # Обновление токена: POST '/api/auth/token'


class STATUS_CODES:
    OK          = 200
    CREATED     = 201
    BAD_REQUEST = 400
    FORBIDDEN   = 403
    NOT_FOUND   = 404
    CONFLICT    = 409


class RESPONSE_KEYS:
    MESSAGE_KEY = 'message'
    OK_KEY      = 'ok'
    ID_KEY      = 'id'
    LOGIN       = 'login'
    PASSWORD    = 'password'
    TRACK       = 'track'
    ORDERS      = 'orders'
    ORDER       = 'order'




