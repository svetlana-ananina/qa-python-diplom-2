class Endpoints:                        # as e
    # URL-адрес сервера
    SERVER_URL = 'https://stellarburgers.nomoreparties.site'
    # Эндпойнты (ручки) запросов к API
    CREATE_USER = '/api/auth/register'      # Регистрация пользователя: POST '/api/auth/register'
    LOGIN_USER = '/api/auth/login'          # Авторизация пользователя: POST '/api/auth/login'
    LOGOUT_USER = '/api/auth/logout'        # Выход из системы: POST '/api/auth/logout', body={"token": "{{refreshToken}}"}
    DELETE_USER = '/api/auth/user'          # Удаление пользователя: DELETE '/api/auth/user'
                                            # headers={"Authorization": "Bearer {auth_token}"}
    GET_USER_DATA = '/api/auth/user'        # Получение данных пользователя: GET '/api/auth/user'
    UPDATE_USER = '/api/auth/user'          # Обновление данных пользователя: PATCH '/api/auth/user'
    GET_INGREDIENTS = '/api/ingredients'    # GET '/api/ingredients'
                                            # ответ: {'success': True, 'data': [{...}, ... ]
    CREATE_ORDER = '/api/orders'            # POST '/api/orders', payload={ "ingredients": ["...","...", ...] }
                                            # ответ: { "name": "...","order": { "number": 6257 }, "success": true }
    GET_USER_ORDERS = '/api/orders'         # GET '/api/orders' (50 последних заказов)

    RESET_PASSWORD = '/api/password-reset/reset'    # POST '/api/password-reset/reset'
                                            # { "password": "", "token": "" }
    UPDATE_TOKEN = '/api/auth/token'        # Обновление токена: POST '/api/auth/token'

    ACCESS_TOKEN_PREFIX = 'Bearer '


class StatusCodes:                  # as CODE
    OK              = 200
    CREATED         = 201
    ACCEPTED        = 202
    BAD_REQUEST     = 400
    UNAUTHORIZED    = 401
    FORBIDDEN       = 403
    NOT_FOUND       = 404
    CONFLICT        = 409
    ERROR_500       = 500           # Internal Server Error


class ResponseKeys:                 # as KEYS
    SUCCESS_KEY     = 'success'
    USER_KEY        = 'user'
    EMAIL_KEY       = 'email'
    NAME_KEY        = 'name'
    ACCESS_TOKEN    = 'accessToken'     # str: "Bearer ..."
    REFRESH_TOKEN   = 'refreshToken'    # str: ""
    MESSAGE_KEY     = 'message'
    DATA            = 'data'            # GET /api/ingredients: 'success': True, 'data': [{...}, ... ]
    INGREDIENTS     = 'ingredients'
    ID_KEY          = '_id'
    TYPE_KEY        = 'type'            # тип ингредиента: "bun", "main", "sauce"
    TYPE_BUN        = 'bun'
    TYPE_MAIN       = 'main'            # основной ингредиент - начинка (filling)
    TYPE_SAUCE      = 'sauce'

    ORDER_KEY       = 'order'
    NUMBER_KEY      = 'number'
    ORDERS_KEY      = 'orders'
    TOTAL_KEY       = 'total'
    TOTAL_TODAY_KEY = 'totalToday'

    # поля для отправки запроса
    AUTH_TOKEN_KEY  = 'Authorization'   # delete: headers
    PASSWORD_KEY    = 'password'
    TOKEN_KEY       = 'token'           # logout: body, ="refreshToken"


class ResponseMessages:             # as message

    LOGOUT                  = 'Successful logout'
    USER_DELETED            = 'User successfully removed'
    PASSWORD_IS_RESET       = 'Password successfully reset'

    USER_ALREADY_EXISTS     = 'User already exists'
    MISSING_REQUIRED_FIELD  = 'Email, password and name are required fields'
    INVALID_LOGIN           = 'email or password are incorrect'
    UNAUTHORIZED            = 'You should be authorised'
    EMAIL_ALREADY_EXISTS    = 'User with such email already exists'
    NO_INGREDIENTS          = 'Ingredient ids must be provided'

