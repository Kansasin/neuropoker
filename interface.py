import os
import config
import game_settings as game
import poker

border = '\n--------------------------------------------------\n'


class Menu:
    def __init__(self, label, options, text_input):
        self.label = label  # может быть как просто строкой, так и функцией, чтобы отображать в меню меняющиеся данные
        self.options = [Option(*x) for x in options]
        self.text_input = text_input

    def get_label(self):
        if type(self.label) == type(lambda: 0): return self.label()
        elif type(self.label) == type(''): return self.label

    def print_menu(self, cls=True):
        if cls: os.system('cls')
        print(self.get_label() + '\n')
        if len(self.options) == 0: return self.text_input.print_input()
        options_str = ''
        for i in range(len(self.options)):
            options_str += f'{i + 1}. {self.options[i].get_text()}\n'
        print('\n' + options_str + '\n')
        self.options[int(self.text_input.print_input()) - 1].callback()


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


def get_cards_string(cards, hide=False):
    string = ''
    for card in cards:
        string += f'[{"XX" if hide else card.icon}] '
    return string

def get_queue_string(hide=True):
    queue = [game.PLAYERS[x] for x in game.CURRENT_QUEUE]
    string = ''
    for player in queue:
        string += f'{player.name} - {"м. блайнд" if player.get_queue_index() == 0 else ("б. блайнд" if player.get_queue_index() == 1 else "игрок")} - {player.bank} ф. - {get_cards_string(player.get_cards(), player.get_index() != game.PLAYERS_NUMBER - 1 and hide)}\n'
    return string

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
    game.ROUND = 0
    menu_list['game_initialization_menu'].print_menu()


def game_preflop_distribution_menu():
    game.ROUND = 0
    menu_list['game_preflop_distribution_menu'].print_menu()


def game_preflop_bet_menu():
    game.ROUND = 1
    menu_list['game_preflop_bet_menu'].print_menu()


def game_flop_distribution_menu():
    game.ROUND = 2
    menu_list['game_flop_distribution_menu'].print_menu()


def game_flop_bet_menu():
    game.ROUND = 3
    menu_list['game_flop_bet_menu'].print_menu()


def game_turn_distribution_menu():
    game.ROUND = 4
    menu_list['game_turn_distribution_menu'].print_menu()


def game_turn_bet_menu():
    game.ROUND = 5
    menu_list['game_turn_bet_menu'].print_menu()


def game_river_distribution_menu():
    game.ROUND = 6
    menu_list['game_river_distribution_menu'].print_menu()


def game_river_bet_menu():
    game.ROUND = 7
    menu_list['game_river_bet_menu'].print_menu()


def game_showdown_menu():
    game.ROUND = 8
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
    if x.isdigit() and 1 <= int(x) <= 5:
        return True
    game_preflop_bet_menu()
    return False

def game_flop_distribution_check(x):
    if x.isdigit() and 1 <= int(x) <= 2:
        return True
    game_flop_distribution_menu()
    return False


def game_flop_bet_check(x):
    if x.isdigit() and 1 <= int(x) <= 5:
        return True
    game_flop_bet_menu()
    return False


def game_turn_distribution_check(x):
    if x.isdigit() and 1 <= int(x) <= 2:
        return True
    game_turn_distribution_menu()
    return False


def game_turn_bet_check(x):
    if x.isdigit() and 1 <= int(x) <= 5:
        return True
    game_turn_bet_menu()
    return False


def game_river_distribution_check(x):
    if x.isdigit() and 1 <= int(x) <= 2:
        return True
    game_river_distribution_menu()
    return False


def game_river_bet_check(x):
    if x.isdigit() and 1 <= int(x) <= 5:
        return True
    game_river_bet_menu()
    return False


def game_showdown_check(x):
    if x.isdigit() and 1 <= int(x) <= 5:
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
        ['Начать игру', game_preflop_distribution_menu],
        ['Вернуться к Настройкам игры', game_settings_menu],
        ['Вернуться в Главное меню', main_menu],
    ], TextInput('Введите номер команды: ', game_initialization_check)),

    'game_preflop_distribution_menu': Menu(lambda: f'Префлоп - раздача - банк {game.BANK}\n\n{get_queue_string()}', [
        ['Продолжить', game_preflop_bet_menu],
        ['Пауза', game_pause_menu],
    ], TextInput('Введите номер команды: ', game_preflop_distribution_check)),
    'game_preflop_bet_menu': Menu(lambda: f'Префлоп - ставки - банк {game.BANK}\n\n{get_queue_string()}', [
        ['Поднять', game_flop_distribution_menu],
        [lambda: 'Уравнять' if True else 'Пропустить', game_flop_distribution_menu],
        ['Ва-банк', game_flop_distribution_menu],
        ['Сбросить', game_flop_distribution_menu],
        ['Пауза', game_pause_menu],
    ], TextInput('Введите номер команды: ', game_preflop_bet_check)),

    'game_flop_distribution_menu': Menu(lambda: f'Флоп - раздача - {get_cards_string(poker.get_table_cards())}- банк {game.BANK}\n\n{get_queue_string()}', [
        ['Продолжить', game_flop_bet_menu],
        ['Пауза', game_pause_menu],
    ], TextInput('Введите номер команды: ', game_preflop_distribution_check)),
    'game_flop_bet_menu': Menu(lambda: f'Флоп - ставки - {get_cards_string(poker.get_table_cards())}- банк {game.BANK}\n\n{get_queue_string()}', [
        ['Поднять', game_turn_distribution_menu],
        [lambda: 'Уравнять' if True else 'Пропустить', game_turn_distribution_menu],
        ['Ва-банк', game_turn_distribution_menu],
        ['Сбросить', game_turn_distribution_menu],
        ['Пауза', game_pause_menu],
    ], TextInput('Введите номер команды: ', game_flop_bet_check)),

    'game_turn_distribution_menu': Menu(lambda: f'Терн - раздача - {get_cards_string(poker.get_table_cards())}- банк {game.BANK}\n\n{get_queue_string()}', [
        ['Продолжить', game_turn_bet_menu],
        ['Пауза', game_pause_menu],
    ], TextInput('Введите номер команды: ', game_turn_distribution_check)),
    'game_turn_bet_menu': Menu(lambda: f'Терн - ставки - {get_cards_string(poker.get_table_cards())}- банк {game.BANK}\n\n{get_queue_string()}', [
        ['Поднять', game_river_distribution_menu],
        [lambda: 'Уравнять' if True else 'Пропустить', game_river_distribution_menu],
        ['Ва-банк', game_river_distribution_menu],
        ['Сбросить', game_river_distribution_menu],
        ['Пауза', game_pause_menu],
    ], TextInput('Введите номер команды: ', game_turn_bet_check)),

    'game_river_distribution_menu': Menu(lambda: f'Ривер - раздача - {get_cards_string(poker.get_table_cards())}- банк {game.BANK}\n\n{get_queue_string()}', [
        ['Продолжить', game_river_bet_menu],
        ['Пауза', game_pause_menu],
    ], TextInput('Введите номер команды: ', game_river_distribution_check)),
    'game_river_bet_menu': Menu(lambda: f'Ривер - ставки - {get_cards_string(poker.get_table_cards())}- банк {game.BANK}\n\n{get_queue_string()}', [
        ['Поднять', game_showdown_menu],
        [lambda: 'Уравнять' if True else 'Пропустить', game_showdown_menu],
        ['Ва-банк', game_showdown_menu],
        ['Сбросить', game_showdown_menu],
        ['Пауза', game_pause_menu],
    ], TextInput('Введите номер команды: ', game_river_bet_check)),

    'game_showdown_menu': Menu(lambda: f'Шоудаун - {get_cards_string(poker.get_table_cards())}- банк {game.BANK}\n\n{get_queue_string(False)}', [
        ['Продолжить', game_initialization_menu],
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
    os.system('color 2')
    os.system('title НейроПокер')
    os.system("mode con cols=75 lines=25")
    main_menu()
