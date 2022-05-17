import os
import config
import game_settings as game
import poker

border = '\n--------------------------------------------------\n'


class Menu:
    def __init__(self, label, options, text_input):
        self.label = label  # может быть как просто строкой, так и функцией, чтобы отображать в меню меняющиеся данные
        self.options = options
        self.text_input = text_input

    def get_label(self):
        if type(self.label) == type(lambda: 0): return self.label()
        elif type(self.label) == type(''): return self.label

    def get_options(self):
        if type(self.options) == type(lambda: 0): return [Option(*x) for x in self.options()]
        elif type(self.options) == type([]): return [Option(*x) for x in self.options]

    def print_menu(self, cls=True):
        if cls: os.system('cls')
        print(self.get_label() + '\n')
        if len(self.get_options()) == 0: return self.text_input.print_input()
        options_str = ''
        for i in range(len(self.get_options())):
            options_str += f'{i + 1}. {self.get_options()[i].get_text()}\n'
        print('\n' + options_str + '\n')
        answer = self.text_input.print_input().split(' ')
        if len(answer) == 1: self.get_options()[int(answer[0]) - 1].callback()  # если функция проверки возвращает только один параметр, то просто вызываем колбэк
        else: self.get_options()[int(answer[0]) - 1].callback(answer)  # если функция проверки возвращает больше параметров, то отдаем их полностью в виде списка


class Option:
    def __init__(self, text, callback):
        self.text = text
        self.callback = callback

    def get_text(self):
        if type(self.text) == type(lambda: 0): return self.text()
        elif type(self.text) == type(''): return self.text


class TextInput:
    def __init__(self, input_text, check):
        self.input_text = input_text  # может быть как просто строкой, так и функцией, чтобы отображать в текстовом поле меняющиеся данные
        self.check = check

    def get_input_text(self):
        if type(self.input_text) == type(lambda: 0): return self.input_text()
        elif type(self.input_text) == type(''): return self.input_text

    def print_input(self):
        is_good = False
        answer = ''
        while not is_good:
            answer = input(self.input_text)
            is_good = self.check(answer)
        return answer


def get_next_round_number():
    return (game.ROUND + 1) % 9


def change_round(round_number=None):
    if not (round_number is None): game.ROUND = round_number
    else: game.ROUND = get_next_round_number() if poker.is_bets_equal() else game.ROUND
    if poker.players_alive() <= 1: game.ROUND = 8
    return game.ROUND


def get_round_menu(round_number):
    return [game_preflop_distribution_menu, game_preflop_bet_menu,
                   game_flop_distribution_menu, game_flop_bet_menu,
                   game_turn_distribution_menu, game_turn_bet_menu,
                   game_river_distribution_menu, game_river_bet_menu,
                   game_showdown_menu, game_initialization_menu][round_number]


def get_user_command_string(command, player):  # возвращает строку для опции по номеру команды и по игроку
    get_string = lambda: ''
    if command == 0: get_string = lambda: f'Поднять <{game.CURRENT_MIN_BET - player.round_bet + 1 if game.GAME_MIN_BET < game.CURRENT_MIN_BET else game.GAME_MIN_BET} - {player.bank - 1}>'
    elif command == 1: get_string = lambda: f'Уравнять ({game.CURRENT_MIN_BET - player.round_bet})'
    elif command == 2: get_string = lambda: 'Пропустить'
    elif command == 3: get_string = lambda: f'Ва-банк ({player.bank})'
    elif command == 4: get_string = lambda: 'Сбросить'
    return get_string


def get_command_string(command):  # возвращает строку комманды
    string = ''
    if command[0] == 0: string = f'Поднял {command[1]}'
    elif command[0] == 1: string = f'Уравнял ({command[1]})'
    elif command[0] == 2: string = 'Пропустил'
    elif command[0] == 3: string = f'Ва-банк ({command[1]})'
    elif command[0] == 4: string = 'Сбросил'
    return string


def raise_command(args):
    game.PLAYERS[-1].exec_command(0, args[1])
    poker.start_query(True)
    return get_round_menu(game.ROUND)()

def blind_command():
    if game.PLAYERS[-1].is_sb: game.PLAYERS[-1].exec_command(0, game.GAME_MIN_BET)
    if game.PLAYERS[-1].is_bb: game.PLAYERS[-1].exec_command(0, game.GAME_MIN_BET * 2)
    poker.start_query(True)
    return get_round_menu(game.ROUND)()

def call_command():
    game.PLAYERS[-1].exec_command(1, 0)
    poker.start_query(True)
    return get_round_menu(game.ROUND)()

def check_command():
    game.PLAYERS[-1].exec_command(2, 0)
    poker.start_query(True)
    return get_round_menu(game.ROUND)()

def allin_command():
    game.PLAYERS[-1].exec_command(3, 0)
    poker.start_query(True)
    return get_round_menu(game.ROUND)()

def fold_command():
    game.PLAYERS[-1].exec_command(4, 0)
    poker.start_query(True)
    return get_round_menu(game.ROUND)()

def continue_command():
    if poker.is_bets_equal():
        change_round()
        poker.reset_round()
    return get_round_menu(game.ROUND)()


def get_available_commands_options():  # возвращает список доступных команд в виде опций для пользователя
    user_commands = [raise_command, call_command, check_command, allin_command, fold_command]

    if game.IS_QUERY_ENDED or game.ROUND % 2 == 0:
        return [['Продолжить', continue_command], ['Пауза', game_pause_menu]]
    elif game.ROUND % 2 == 1:
        if game.ROUND == 1 and game.PLAYERS[-1].round_bet == 0 and (game.PLAYERS[-1].is_sb or game.PLAYERS[-1].is_bb):
            if game.PLAYERS[-1].is_sb: return [[f'Поднять {game.GAME_MIN_BET}', blind_command], ['Пауза', game_pause_menu]]
            if game.PLAYERS[-1].is_bb: return [[f'Поднять {game.GAME_MIN_BET * 2}', blind_command], ['Пауза', game_pause_menu]]
        return [[get_user_command_string(command, game.PLAYERS[-1]), user_commands[command]] for command in poker.get_available_commands_number(game.PLAYERS[-1])] + [['Пауза', game_pause_menu]]


def get_cards_string(cards, hide=False):
    string = ''
    for card in cards:
        string += f'[{"XX" if hide else card.icon}] '
    return string


def get_queue_string():
    queue = [game.PLAYERS[x] for x in game.INITIAL_QUEUE]
    string = ''
    for player in queue:
        cards = get_cards_string(player.get_cards(), (game.ROUND != 8) and (player.get_index() != game.PLAYERS_NUMBER - 1))
        string += f'{player.name} - {player.get_role()} - {player.bank} ф. - {cards}\n'
    return string


def get_queue_commands_string():  # тоже, что и get_queue_string(), только каждая строка содержит команды, которые сделали игроки
    poker.start_query(False)
    queue = [(game.PLAYERS[record[1]], (record[2], record[3])) for record in game.HISTORY_QUEUE if record[0] == game.ROUND]
    string = ''
    for player, command in queue:
        cards = get_cards_string(player.get_cards(), (game.ROUND == 8) or (player.get_index() != game.PLAYERS_NUMBER - 1))
        string += f'{player.name} - {player.get_role()} - {player.bank} ф. - {cards}: {get_command_string(command)}\n'

    cards = get_cards_string(game.PLAYERS[-1].get_cards(), game.ROUND == 8)
    return string + f'{game.PLAYERS[-1].name} - {game.PLAYERS[-1].get_role()} - {game.PLAYERS[-1].bank} ф. - {cards}:\n'


def main_menu():
    menu_list['main_menu'].print_menu()


def learn_settings_menu():
    menu_list['learn_settings_menu'].print_menu()


def game_settings_menu():
    menu_list['game_settings_menu'].print_menu()


def db_settings_menu():
    menu_list['db_settings_menu'].print_menu()


def learning_players_number_menu():
    menu_list['learning_players_number_menu'].print_menu()


def series_length_menu():
    menu_list['series_length_menu'].print_menu()


def series_number_menu():
    menu_list['series_number_menu'].print_menu()


def autosaves_frequency_menu():
    menu_list['autosaves_frequency_menu'].print_menu()


def start_learning_menu():
    menu_list['start_learning_menu'].print_menu()


def players_number_menu():
    menu_list['players_number_menu'].print_menu()


def bots_names_menu():
    menu_list['bots_names_menu'].print_menu()


def min_bet_menu():
    menu_list['min_bet_menu'].print_menu()


def rules_menu():
    menu_list['rules_menu'].print_menu()


def import_db_menu():
    menu_list['import_db_menu'].print_menu()


def export_db_menu():
    menu_list['export_db_menu'].print_menu()


def erase_db_menu():
    menu_list['erase_db_menu'].print_menu()


def game_initialization_menu():
    menu_list['game_initialization_menu'].print_menu()


def game_preflop_distribution_menu():
    menu_list['game_preflop_distribution_menu'].print_menu()


def game_preflop_bet_menu():
    menu_list['game_preflop_bet_menu'].print_menu()


def game_flop_distribution_menu():
    menu_list['game_flop_distribution_menu'].print_menu()


def game_flop_bet_menu():
    menu_list['game_flop_bet_menu'].print_menu()


def game_turn_distribution_menu():
    menu_list['game_turn_distribution_menu'].print_menu()


def game_turn_bet_menu():
    menu_list['game_turn_bet_menu'].print_menu()


def game_river_distribution_menu():
    menu_list['game_river_distribution_menu'].print_menu()


def game_river_bet_menu():
    menu_list['game_river_bet_menu'].print_menu()


def game_showdown_menu():
    menu_list['game_showdown_menu'].print_menu()


def game_pause_menu():
    menu_list['game_pause_menu'].print_menu()


def return_to_game():
    rounds = [  'game_preflop_distribution_menu', 'game_preflop_bet_menu',
                'game_flop_distribution_menu', 'game_flop_bet_menu',
                'game_turn_distribution_menu', 'game_turn_bet_menu',
                'game_river_distribution_menu', 'game_river_bet_menu',
                'game_showdown_menu']
    menu_list[rounds[game.ROUND]].print_menu()


def pause_rules_menu():
    menu_list['pause_rules_menu'].print_menu()


def learning_bots_number_check(x):
    if not x.isdigit() or x == '':
        learn_settings_menu()
        return True
    elif 1 <= int(x) <= 10:
        game.PLAYERS_NUMBER = int(x)
        learn_settings_menu()
        return True
    return False


def series_length_check(x):
    if not x.isdigit() or x == '':
        learn_settings_menu()
        return True
    elif 1 <= int(x) <= 30:
        config.SERIES_LENGTH = int(x)
        learn_settings_menu()
        return True
    return False


def series_number_check(x):
    if not x.isdigit() or x == '':
        learn_settings_menu()
        return True
    elif 1 <= int(x) <= 10000000:
        config.SERIES_NUMBER = int(x)
        learn_settings_menu()
        return True
    return False


def autosaves_frequency_check(x):
    if not x.isdigit() or x == '':
        learn_settings_menu()
        return True
    elif 1 <= int(x) <= 120:
        config.AUTOSAVES_FREQUENCY = int(x)
        learn_settings_menu()
        return True
    return False


def bots_number_check(x):
    if not x.isdigit() or x == '':
        game_settings_menu()
        return True
    elif 2 <= int(x) <= 10:
        game.PLAYERS_NUMBER = int(x)
        game_settings_menu()
        return True
    return False


def bots_names_check(x):
    if not x.isdigit() or x == '':
        game_settings_menu()
        return True
    elif False in [len(name) < 15 for name in x.split()]:
        config.BOTS_NAMES = x
        game_settings_menu()
        return True
    print(x)
    return False


def min_bet_check(x):
    if not x.isdigit() or x == '':
        game_settings_menu()
        return True
    elif 50 <= int(x) <= 1000000:
        game.GAME_MIN_BET = int(x)
        game_settings_menu()
        return True
    return False


def rules_check(x):
    if len(x) >= 0:
        game_settings_menu()
        return True
    return False


def import_db_check(x):
    if len(x) >= 0:  # сделать проверку на существование пути
        # сделать импорт заданного файла в текущую базу данных
        db_settings_menu()
        return True
    return False


def export_db_check(x):
    if len(x) >= 0:  # сделать проверку на существование пути
        # сделать экспорт по заданному пути текущей базы данных
        db_settings_menu()
        return True
    return False


def erase_db_check(x):
    if x == '' or x.lower() in ['y', 'n', 'yes', 'no', 'д', 'н', 'да', 'нет']:
        # сделать сброс базы данных
        db_settings_menu()
        return True
    return False


def main_check(x):
    if x.isdigit() and 1 <= int(x) <= 3:
        return True
    main_menu()
    return False


def learn_settings_check(x):
    if x.isdigit() and 1 <= int(x) <= 7:
        return True
    learn_settings_menu()
    return False


def game_settings_check(x):
    if x.isdigit() and 1 <= int(x) <= 6:
        return True
    game_settings_menu()
    return False


def db_settings_check(x):
    if x.isdigit() and 1 <= int(x) <= 5:
        return True
    db_settings_menu()
    return False


def game_initialization_check(x):
    if x.isdigit() and 1 <= int(x) <= 3:
        poker.set_game()
        return True
    game_initialization_menu()
    return False


def game_preflop_distribution_check(x):
    if x.isdigit() and 1 <= int(x) <= 2:
        return True
    game_preflop_distribution_menu()
    return False


def game_preflop_bet_check(x):
    x = x.split(' ')
    if x[0].isdigit() and 1 <= int(x[0]) <= 6:  # TODO: сделать проверку количества опций динамичной
        return True
    game_preflop_bet_menu()
    return False


def game_flop_distribution_check(x):
    if x.isdigit() and 1 <= int(x) <= 2:
        return True
    game_flop_distribution_menu()
    return False


def game_flop_bet_check(x):
    x = x.split(' ')
    if x[0].isdigit() and 1 <= int(x[0]) <= 6:
        return True
    game_flop_bet_menu()
    return False


def game_turn_distribution_check(x):
    if x.isdigit() and 1 <= int(x) <= 2:
        return True
    game_turn_distribution_menu()
    return False


def game_turn_bet_check(x):
    x = x.split(' ')
    if x[0].isdigit() and 1 <= int(x[0]) <= 6:
        return True
    game_turn_bet_menu()
    return False


def game_river_distribution_check(x):
    if x.isdigit() and 1 <= int(x) <= 2:
        return True
    game_river_distribution_menu()
    return False


def game_river_bet_check(x):
    x = x.split(' ')
    if x[0].isdigit() and 1 <= int(x[0]) <= 6:
        return True
    game_river_bet_menu()
    return False


def game_showdown_check(x):
    if x.isdigit() and 1 <= int(x) <= 2:
        return True
    game_showdown_menu()
    return False


def pause_rules_check(x):
    if len(x) >= 0:
        game_pause_menu()
        return True
    return False


menu_list = {
    # '': Menu('', [], TextInput('', lambda x: x)),
    'main_menu': Menu('Главное меню:', [
        ['Игра с ботами', game_settings_menu],
        ['Обучение ботов', learn_settings_menu],
        ['Завершение программы', exit]
    ], TextInput('Выберите номер команды: ', main_check)),

    'learn_settings_menu': Menu('Настройки обучения:', [
        ['Настройки базы данных', db_settings_menu],
        ['Количество ботов', learning_players_number_menu],
        ['Длина серии игр', series_length_menu],
        ['Количество обучающих серий', series_number_menu],
        ['Частота автосохранений', autosaves_frequency_menu],
        ['Начать обучение', start_learning_menu],
        ['Вернуться в Главное меню', main_menu]
    ], TextInput('Выберите номер команды: ', learn_settings_check)),
    'learning_players_number_menu': Menu(lambda: f'Настройки обучения: Количество ботов - {game.PLAYERS_NUMBER}', [], TextInput('Введите количество ботов (1-10): ', learning_bots_number_check)),
    'series_length_menu': Menu(lambda: f'Настройки обучения: Длина серии игр - {config.SERIES_LENGTH}', [], TextInput('Введите длину серии игр (1-30): ', series_length_check)),
    'series_number_menu': Menu(lambda: f'Настройки обучения: Количество серий игр - {config.SERIES_NUMBER}', [], TextInput('Введите количество обучающих серий (1-10000000): ', series_number_check)),
    'autosaves_frequency_menu': Menu(lambda: f'Настройки обучения: Частота автосохранений - {config.AUTOSAVES_FREQUENCY}', [], TextInput('Введите частоту автосохранений (до 120 минут): ', autosaves_frequency_check)),

    'game_settings_menu': Menu('Настройки игры:', [
        ['Количество игроков', players_number_menu],
        ['Имена ботов', bots_names_menu],
        ['Минимальная ставка', min_bet_menu],
        ['Правила игры', rules_menu],
        ['Начать игру', game_initialization_menu],
        ['Вернуться в Главное меню', main_menu]
    ], TextInput('Выберите номер команды: ', game_settings_check)),
    'players_number_menu': Menu(lambda: f'Настройки игры: Количество игроков - {game.PLAYERS_NUMBER}', [], TextInput('Введите количество игроков (2-10): ', bots_number_check)),
    'bots_names_menu': Menu('Настройки игры: Имена ботов', [], TextInput('Введите новые имена ботов через пробел: ', bots_names_check)),
    'min_bet_menu': Menu(lambda: f'Настройки игры: Минимальная ставка - {game.GAME_MIN_BET}', [], TextInput('Введите минимальную ставку (50-1000000): ', min_bet_check)),
    'rules_menu': Menu(lambda: f'Настройки игры: Правила игры - {config.RULES}', [], TextInput('Введите Хоп-хей-ла-лей, чтобы продолжить: ', rules_check)),

    'db_settings_menu': Menu('Настройки базы данных', [
        ['Импорт базы данных', import_db_menu],
        ['Экспорт базы данных', export_db_menu],
        ['Очистка базы данных', erase_db_menu],
        ['Вернуться в Настройки обучения', game_settings_menu],
        ['Вернуться в Главное меню', main_menu],
    ], TextInput('Выберите номер команды: ', db_settings_check)),
    'import_db_menu': Menu(lambda: f'Настройки базы данных: Путь до последнего импортированного файла базы данных - {config.IMPORT_PATH}', [], TextInput('Введите путь до импортируемой базы данных: ', import_db_check)),
    'export_db_menu': Menu(lambda: f'Настройки базы данных: Путь до последнего экпортированного файла базы данных - {config.EXPORT_PATH}', [], TextInput('Введите путь сохранения базы данных: ', export_db_check)),
    'erase_db_menu': Menu(lambda: f'Настройки базы данных: Очистка файла базы данных - {config.DB_PATH}', [], TextInput('Файл базы данных будет очищен. Вы уверены? ', erase_db_check)),

    'game_initialization_menu': Menu(lambda: f'Настройка...\nКоличество игроков: {game.PLAYERS_NUMBER}\nМинимальная ставка: {game.GAME_MIN_BET}\nВремя обучения ботов: {config.BOTS_LEARNING_SERIES_LENGTH}', [
        ['Начать игру', get_round_menu(0)],
        ['Вернуться к Настройкам игры', game_settings_menu],
        ['Вернуться в Главное меню', main_menu],
    ], TextInput('Введите номер команды: ', game_initialization_check)),

    'game_preflop_distribution_menu': Menu(lambda: f'Префлоп - раздача - банк {poker.get_bank()}\n\n' + get_queue_string(),
                                lambda: get_available_commands_options(),
                                TextInput('Введите номер команды: ', game_preflop_distribution_check)),
    'game_preflop_bet_menu': Menu(lambda: f'Префлоп - ставки - банк {poker.get_bank()}\n\n' + get_queue_commands_string(),
                                lambda: get_available_commands_options(),
                                TextInput('Введите номер команды: ', game_preflop_bet_check)),

    'game_flop_distribution_menu': Menu(lambda: f'Флоп - раздача - {get_cards_string(poker.get_table_cards())}- банк {poker.get_bank()}\n\n' + get_queue_string(),
                                lambda: get_available_commands_options(),
                                TextInput('Введите номер команды: ', game_preflop_distribution_check)),
    'game_flop_bet_menu': Menu(lambda: f'Флоп - ставки - {get_cards_string(poker.get_table_cards())}- банк {poker.get_bank()}\n\n' + get_queue_commands_string(),
                                lambda: get_available_commands_options(),
                                TextInput('Введите номер команды: ', game_flop_bet_check)),

    'game_turn_distribution_menu': Menu(lambda: f'Терн - раздача - {get_cards_string(poker.get_table_cards())}- банк {poker.get_bank()}\n\n' + get_queue_string(),
                                lambda: get_available_commands_options(),
                                TextInput('Введите номер команды: ', game_turn_distribution_check)),
    'game_turn_bet_menu': Menu(lambda: f'Терн - ставки - {get_cards_string(poker.get_table_cards())}- банк {poker.get_bank()}\n\n' + get_queue_commands_string(),
                               lambda: get_available_commands_options(),
                               TextInput('Введите номер команды: ', game_turn_bet_check)),

    'game_river_distribution_menu': Menu(lambda: f'Ривер - раздача - {get_cards_string(poker.get_table_cards())}- банк {poker.get_bank()}\n\n' + get_queue_string(),
                               lambda: get_available_commands_options(),
                               TextInput('Введите номер команды: ', game_river_distribution_check)),
    'game_river_bet_menu': Menu(lambda: f'Ривер - ставки - {get_cards_string(poker.get_table_cards())}- банк {poker.get_bank()}\n\n' + get_queue_commands_string(),
                                lambda: get_available_commands_options(),
                                TextInput('Введите номер команды: ', game_river_bet_check)),

    'game_showdown_menu': Menu(lambda: f'Шоудаун - {get_cards_string(poker.get_table_cards())}- банк {poker.get_bank()}\n\n' + get_queue_string(), [
        ['Завершить', game_initialization_menu],
        ['Пауза', game_pause_menu],
    ], TextInput('Введите номер команды: ', game_showdown_check)),

    'game_pause_menu': Menu(f'Пауза', [
        ['Продолжить', return_to_game],
        ['Помощь', pause_rules_menu],
        ['Вернуться в Главное меню', main_menu],
    ], TextInput('Введите номер команды: ', lambda x: x)),
    'pause_rules_menu': Menu(lambda: f'Пауза: Правила игры - {config.RULES}', [], TextInput('Введите Хоп-хей-ла-лей, чтобы продолжить: ', pause_rules_check)),
}


def start():
    main_menu()
