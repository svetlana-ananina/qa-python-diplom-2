_to_print = True
# _to_print = False

# URL-адрес сервера
SERVER_URL = 'https://stellarburgers.nomoreparties.site'

# Эндпойнты (ручки) запросов к API
CREATE_USER = '/api/auth/register'  # Регистрация пользователя: POST '/api/auth/register'
LOGIN_USER = '/api/auth/login'      # Авторизация пользователя: POST '/api/auth/login'
LOGOUT_USER = '/api/auth/logout'    # Выход из системы: POST '/api/auth/logout', body={"token": "{{refreshToken}}"}
DELETE_USER = '/api/auth/user'      # Удаление пользователя: DELETE '/api/auth/user'
                                    # headers={"Authorization": "Bearer {auth_token}"}
                                    # response=<Response [202]>, text={"success":true,"message":"User successfully removed"}
GET_USER_DATA = '/api/auth/user'    # Получение данных пользователя: GET '/api/auth/user'
UPDATE_USER = '/api/auth/user'      # Обновление данных пользователя: PATCH '/api/auth/user'

UPDATE_TOKEN = '/api/auth/token'    # Обновление токена: POST '/api/auth/token'


class STATUS_CODES:
    OK              = 200
    CREATED         = 201
    ACCEPTED        = 202
    BAD_REQUEST     = 400
    UNAUTHORIZED    = 401
    FORBIDDEN       = 403
    NOT_FOUND       = 404
    CONFLICT        = 409


class RESPONSE_KEYS:
    SUCCESS_KEY     = 'success'
    USER_KEY        = 'user'
    EMAIL_KEY       = 'email'
    NAME_KEY        = 'name'
    ACCESS_TOKEN    = 'accessToken'     # str: "Bearer ..."
    REFRESH_TOKEN   = 'refreshToken'    # str: ""
    MESSAGE_KEY     = 'message'

    # поля для отправки запроса
    AUTH_TOKEN      = 'Authorization'       # delete: headers
    PASSWORD_KEY    = 'password'
    TOKEN           = 'token'               # logout: body, ="refreshToken"


ACCESS_TOKEN_PREFIX = "Bearer "


class RESPONSE_MESSAGES:
    LOGOUT                  = 'Successful logout'
    USER_DELETED            = 'User successfully removed'

    USER_ALREADY_EXISTS     = 'User already exists'
    MISSING_REQUIRED_FIELD  = 'Email, password and name are required fields'
    INVALID_LOGIN           = 'email or password are incorrect'
    UNAUTHORIZED            = 'You should be authorised'
    EMAIL_ALREADY_EXISTS    = 'User with such email already exists'

    #OK_KEY      = 'ok'
    #ID_KEY      = 'id'
    #LOGIN       = 'login'
    #PASSWORD    = 'password'
    #TRACK       = 'track'
    #ORDERS      = 'orders'
    #ORDER       = 'order'




