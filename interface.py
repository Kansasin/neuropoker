import os
import config
import game_settings as game

border = '\n--------------------------------------------------\n'


class Menu:
    def __init__(self, label, options, text_input, current_value_func=None):  # переделать отображение label (проверка фукнции или строки)
        self.label = label
        self.options = [Option(*x) for x in options]
        self.text_input = text_input
        self.current_value_func = current_value_func

    def get_label(self):
        return f'{self.label}{" - " if self.current_value_func else ""}{self.current_value_func() if self.current_value_func else ""}'

    def print_menu(self, cls=True):
        if cls: os.system('cls')
        print(self.get_label() + '\n')
        if len(self.options) == 0: return self.text_input.print_input()
        options_str = ''
        for i in range(len(self.options)):
            options_str += f'{i + 1}. {self.options[i].text}\n'
        print('\n' + options_str + '\n')
        self.options[int(self.text_input.print_input()) - 1].callback()


class Option:
    def __init__(self, text, callback):
        self.text = text
        self.callback = callback


class TextInput:
    def __init__(self, input_text, check):
        self.input_text = input_text
        self.check = check

    def print_input(self):
        is_good = False
        while not is_good:
            answer = input(self.input_text)
            is_good = self.check(answer)
        return answer


def main_menu():
    menu_list['main_menu'].print_menu()


def learn_settings_menu():
    menu_list['learn_settings_menu'].print_menu()


def game_settings_menu():
    menu_list['game_settings_menu'].print_menu()


def db_settings_menu():
    menu_list['db_settings_menu'].print_menu()


def learning_bots_number_menu():
    menu_list['learning_bots_number_menu'].print_menu()


def series_length_menu():
    menu_list['series_length_menu'].print_menu()


def series_number_menu():
    menu_list['series_number_menu'].print_menu()


def autosaves_frequency_menu():
    menu_list['autosaves_frequency_menu'].print_menu()


def start_learning_menu():
    menu_list['start_learning_menu'].print_menu()


def bots_number_menu():
    menu_list['bots_number_menu'].print_menu()


def bots_names_menu():
    menu_list['bots_names_menu'].print_menu()


def min_bet_menu():
    menu_list['min_bet_menu'].print_menu()


def rules_menu():
    menu_list['rules_menu'].print_menu()


def start_play():
    menu_list['start_play'].print_menu()


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
        config.BOTS_NUMBER = int(x)
        config.PLAYERS_NUMBER = int(x)
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
    elif 1 <= int(x) <= 9:
        config.BOTS_NUMBER = int(x)
        config.PLAYERS_NUMBER = int(x) + 1
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
        config.MIN_BET = int(x)
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
        ['Количество ботов', learning_bots_number_menu],
        ['Длина серии игр', series_length_menu],
        ['Количество обучающих серий', series_number_menu],
        ['Частота автосохранений', autosaves_frequency_menu],
        ['Начать обучение', start_learning_menu],
        ['Вернуться в Главное меню', main_menu]
    ], TextInput('Выберите номер команды: ', learn_settings_check)),
    'learning_bots_number_menu': Menu(f'Настройки обучения: Количество ботов', [], TextInput('Введите количество ботов (1-10): ', learning_bots_number_check), lambda: config.PLAYERS_NUMBER),
    'series_length_menu': Menu(f'Настройки обучения: Длина серии игр', [], TextInput('Введите длину серии игр (1-30): ', series_length_check), lambda: config.SERIES_LENGTH),
    'series_number_menu': Menu(f'Настройки обучения: Количество серий игр', [], TextInput('Введите количество обучающих серий (1-10000000): ', series_number_check), lambda: config.SERIES_NUMBER),
    'autosaves_frequency_menu': Menu('Настройки обучения: Частота автосохранений', [], TextInput('Введите частоту автосохранений (до 120 минут): ', autosaves_frequency_check), lambda: config.AUTOSAVES_FREQUENCY),

    'game_settings_menu': Menu('Настройки игры:', [
        ['Количество ботов', bots_number_menu],
        ['Имена ботов', bots_names_menu],
        ['Минимальная ставка', min_bet_menu],
        ['Правила игры', rules_menu],
        ['Начать игру', game_initialization_menu],
        ['Вернуться в Главное меню', main_menu]
    ], TextInput('Выберите номер команды: ', game_settings_check)),
    'bots_number_menu': Menu(f'Настройки игры: Количество ботов', [], TextInput('Введите количество ботов (1-9): ', bots_number_check), lambda: config.BOTS_NUMBER),
    'bots_names_menu': Menu('Настройки игры: Имена ботов', [], TextInput('Введите новые имена ботов через пробел: ', bots_names_check)),
    'min_bet_menu': Menu(f'Настройки игры: Минимальная ставка', [], TextInput('Введите минимальную ставку (50-1000000): ', min_bet_check), lambda: game.GAME_MIN_BET),
    'rules_menu': Menu('Настройки игры: Правила игры', [], TextInput('Введите Хоп-хей-ла-лей, чтобы продолжить: ', rules_check), lambda: config.RULES),

    'db_settings_menu': Menu('Настройки базы данных', [
        ['Импорт базы данных', import_db_menu],
        ['Экспорт базы данных', export_db_menu],
        ['Очистка базы данных', erase_db_menu],
        ['Вернуться в Настройки обучения', game_settings_menu],
        ['Вернуться в Главное меню', main_menu],
    ], TextInput('Выберите номер команды: ', db_settings_check)),
    'import_db_menu': Menu('Настройки базы данных: Путь до последнего импортированного файла базы данных', [], TextInput('Введите путь до импортируемой базы данных: ', import_db_check), lambda: config.IMPORT_PATH),
    'export_db_menu': Menu('Настройки базы данных: Путь до последнего экпортированного файла базы данных', [], TextInput('Введите путь сохранения базы данных: ', export_db_check), lambda: config.EXPORT_PATH),
    'erase_db_menu': Menu('Настройки базы данных: Очистка файла базы данных', [], TextInput('Файл базы данных будет очищен. Вы уверены? ', erase_db_check), lambda: config.DB_PATH),

    'game_initialization_menu': Menu(f'Настройка...\nОчередь: {game.INITIAL_QUEUE}\nМинимальная ставка: {game.GAME_MIN_BET}\nВремя обучения ботов: {config.BOTS_LEARNING_SERIES_LENGTH}', [
        ['Начать игру', game_preflop_distribution_menu],
        ['Вернуться к Настройкам игры', game_settings_menu],
        ['Вернуться в Главное меню', main_menu],
    ], TextInput('Введите номер команды: ', game_initialization_check)),
    'game_preflop_distribution_menu': Menu(f'Префлоп - раздача - банк', [
        ['Продолжить', game_preflop_bet_menu],
        ['Пауза', game_pause_menu],
    ], TextInput('Введите номер команды: ', game_preflop_distribution_check), lambda: game.BANK),
    'game_preflop_bet_menu': Menu(f'Префлоп - ставки - банк', [
        ['Поднять', game_flop_distribution_menu],
        ['Уравнять', game_flop_distribution_menu],
        ['Ва-банк', game_flop_distribution_menu],
        ['Сбросить', game_flop_distribution_menu],
        ['Пауза', game_pause_menu],
    ], TextInput('Введите номер команды: ', game_preflop_bet_check), lambda: game.BANK),

    'game_pause_menu': Menu(f'Пауза', [
        ['Продолжить', return_to_game],
        ['Помощь', pause_rules_menu],
        ['Вернуться в Главное меню', main_menu],
    ], TextInput('Введите номер команды: ', lambda x: x)),
    'pause_rules_menu': Menu('Правила игры', [], TextInput('Введите Хоп-хей-ла-лей, чтобы продолжить: ', pause_rules_check), lambda: config.RULES),
}


def start():
    os.system('color 2')
    os.system('title НейроПокер')
    os.system("mode con cols=75 lines=25")
    main_menu()
