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
GET_USER_DATA = '/api/auth/user'    # Получение данных пользователя: GET '/api/auth/user'
UPDATE_USER = '/api/auth/user'      # Обновление данных пользователя: PATCH '/api/auth/user'
GET_INGREDIENTS = '/api/ingredients'   # GET '/api/ingredients'
                                    # ответ: {'success': True, 'data': [{...}, ... ]
CREATE_ORDER = '/api/orders'        # POST '/api/orders', payload={ "ingredients": ["...","...", ...] }
                                    # ответ: { "name": "...","order": { "number": 6257 }, "success": true }
GET_USER_ORDERS = '/api/orders'     # GET '/api/orders' (50 последних заказов)

RESET_PASSWORD = '/api/password-reset/reset'    # POST '/api/password-reset/reset'
                                                # { "password": "", "token": "" }
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
    ERROR_500       = 500       # Internal Server Error


class RESPONSE_KEYS:

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


    # поля для отправки запроса
    AUTH_TOKEN_KEY  = 'Authorization'   # delete: headers
    PASSWORD_KEY    = 'password'
    TOKEN_KEY       = 'token'           # logout: body, ="refreshToken"


ACCESS_TOKEN_PREFIX = "Bearer "


class RESPONSE_MESSAGES:

    LOGOUT                  = 'Successful logout'
    USER_DELETED            = 'User successfully removed'
    PASSWORD_IS_RESET       = 'Password successfully reset'

    USER_ALREADY_EXISTS     = 'User already exists'
    MISSING_REQUIRED_FIELD  = 'Email, password and name are required fields'
    INVALID_LOGIN           = 'email or password are incorrect'
    UNAUTHORIZED            = 'You should be authorised'
    EMAIL_ALREADY_EXISTS    = 'User with such email already exists'
    NO_INGREDIENTS          = 'Ingredient ids must be provided'

    #OK_KEY      = 'ok'
    #ID_KEY      = 'id'
    #LOGIN       = 'login'
    #PASSWORD    = 'password'
    #TRACK       = 'track'
    #ORDERS      = 'orders'
    #ORDER       = 'order'


INGREDIENTS_LIST = [
        {
            "_id": "61c0c5a71d1f82001bdaaa6d",
            "name": "Флюоресцентная булка R2-D3",
            "type": "bun",
            "proteins": 44,
            "fat": 26,
            "carbohydrates": 85,
            "calories": 643,
            "price": 988,
            "image": "https://code.s3.yandex.net/react/code/bun-01.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/bun-01-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/bun-01-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa6f",
            "name": "Мясо бессмертных моллюсков Protostomia",
            "type": "main",
            "proteins": 433,
            "fat": 244,
            "carbohydrates": 33,
            "calories": 420,
            "price": 1337,
            "image": "https://code.s3.yandex.net/react/code/meat-02.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/meat-02-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/meat-02-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa70",
            "name": "Говяжий метеорит (отбивная)",
            "type": "main",
            "proteins": 800,
            "fat": 800,
            "carbohydrates": 300,
            "calories": 2674,
            "price": 3000,
            "image": "https://code.s3.yandex.net/react/code/meat-04.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/meat-04-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/meat-04-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa71",
            "name": "Биокотлета из марсианской Магнолии",
            "type": "main",
            "proteins": 420,
            "fat": 142,
            "carbohydrates": 242,
            "calories": 4242,
            "price": 424,
            "image": "https://code.s3.yandex.net/react/code/meat-01.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/meat-01-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/meat-01-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa72",
            "name": "Соус Spicy-X",
            "type": "sauce",
            "proteins": 30,
            "fat": 20,
            "carbohydrates": 40,
            "calories": 30,
            "price": 90,
            "image": "https://code.s3.yandex.net/react/code/sauce-02.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/sauce-02-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/sauce-02-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa6e",
            "name": "Филе Люминесцентного тетраодонтимформа",
            "type": "main",
            "proteins": 44,
            "fat": 26,
            "carbohydrates": 85,
            "calories": 643,
            "price": 988,
            "image": "https://code.s3.yandex.net/react/code/meat-03.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/meat-03-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/meat-03-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa73",
            "name": "Соус фирменный Space Sauce",
            "type": "sauce",
            "proteins": 50,
            "fat": 22,
            "carbohydrates": 11,
            "calories": 14,
            "price": 80,
            "image": "https://code.s3.yandex.net/react/code/sauce-04.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/sauce-04-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/sauce-04-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa74",
            "name": "Соус традиционный галактический",
            "type": "sauce",
            "proteins": 42,
            "fat": 24,
            "carbohydrates": 42,
            "calories": 99,
            "price": 15,
            "image": "https://code.s3.yandex.net/react/code/sauce-03.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/sauce-03-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/sauce-03-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa6c",
            "name": "Краторная булка N-200i",
            "type": "bun",
            "proteins": 80,
            "fat": 24,
            "carbohydrates": 53,
            "calories": 420,
            "price": 1255,
            "image": "https://code.s3.yandex.net/react/code/bun-02.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/bun-02-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/bun-02-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa75",
            "name": "Соус с шипами Антарианского плоскоходца",
            "type": "sauce",
            "proteins": 101,
            "fat": 99,
            "carbohydrates": 100,
            "calories": 100,
            "price": 88,
            "image": "https://code.s3.yandex.net/react/code/sauce-01.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/sauce-01-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/sauce-01-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa76",
            "name": "Хрустящие минеральные кольца",
            "type": "main",
            "proteins": 808,
            "fat": 689,
            "carbohydrates": 609,
            "calories": 986,
            "price": 300,
            "image": "https://code.s3.yandex.net/react/code/mineral_rings.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/mineral_rings-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/mineral_rings-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa77",
            "name": "Плоды Фалленианского дерева",
            "type": "main",
            "proteins": 20,
            "fat": 5,
            "carbohydrates": 55,
            "calories": 77,
            "price": 874,
            "image": "https://code.s3.yandex.net/react/code/sp_1.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/sp_1-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/sp_1-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa78",
            "name": "Кристаллы марсианских альфа-сахаридов",
            "type": "main",
            "proteins": 234,
            "fat": 432,
            "carbohydrates": 111,
            "calories": 189,
            "price": 762,
            "image": "https://code.s3.yandex.net/react/code/core.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/core-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/core-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa79",
            "name": "Мини-салат Экзо-Плантаго",
            "type": "main",
            "proteins": 1,
            "fat": 2,
            "carbohydrates": 3,
            "calories": 6,
            "price": 4400,
            "image": "https://code.s3.yandex.net/react/code/salad.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/salad-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/salad-large.png",
            "__v": 0
        },
        {
            "_id": "61c0c5a71d1f82001bdaaa7a",
            "name": "Сыр с астероидной плесенью",
            "type": "main",
            "proteins": 84,
            "fat": 48,
            "carbohydrates": 420,
            "calories": 3377,
            "price": 4142,
            "image": "https://code.s3.yandex.net/react/code/cheese.png",
            "image_mobile": "https://code.s3.yandex.net/react/code/cheese-mobile.png",
            "image_large": "https://code.s3.yandex.net/react/code/cheese-large.png",
            "__v": 0
        }
    ]


