PLAYERS = []  # игроки (сначала боты, потом пользователь)
INITIAL_QUEUE = []  # начальная очередность ходов при старте игры (число означает индекс игрока в PLAYERS)
HISTORY_QUEUE = []  # история ходов за каждый раунд, где запись состоит из: номера раунда, индекса игрока, команды игрока и ставки
LAST_RAISER = None  # последний поднявший ставку (индекс), None - если никто не поднимал
CURRENT_MIN_BET = 100  # текущая минимальная ставка
COMMON_CARDS = []  # общие карты
BANK = 0  # текущий банк
ROUND = 0  # текущий раунд: 0 - раздача на префлопе, 1 - ставки на префлопе, 2-3 - флоп, 4-5 - терн, 6-7 - ривер, 8 - шоудаун
ROUND_STEP = 0  # раунд ставок в раунде ставок. Да.
CARDS = []  # карты: первые 20 карт на 10 игроков и последние 5 карт на столе
IS_QUERY_ENDED = False  # флаг окончания опроса игроков, необходимый для определения завершения раунда
GAME_WAS_INITIALIZED = False  # флаг факта инициализации игры (нужен для полной или частичной очистки данных об игре)
GAME_WITH_USER = False  # игра с пользователем или без

SAVABLE = {
    'MIN_BANK': 1000,  # количество фишек игрока по умолчанию
    'GAME_MIN_BET': 100,  # минимальная ставка игры
    'PLAYERS_NUMBER': 3,  # количество игроков в игре
    'STD_BOTS_NAMES': 'Oleg Igor Anton Pavel Alexander Egor Ivan Konstantin Ilya Denis Andrey Artem Vlad Vadim Viktor Danil Dmitriy Grigoriy Georgiy Maksim',  # допустимые имена ботов через пробел
    'USR_BOTS_NAMES': '',  # пользовательские имена для ботов
    'BOTS_MODE': 'passive'  # сложность ботов: passive - пассивные боты, random - боты со случайным поведением, trained - обученные боты
}





