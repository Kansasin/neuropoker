import train_settings
import game_settings as game
import poker
from file import File
from menu import *


def get_round_menu(round_number):
    return [game_preflop_distribution_menu, game_preflop_bet_menu,
                   game_flop_distribution_menu, game_flop_bet_menu,
                   game_turn_distribution_menu, game_turn_bet_menu,
                   game_river_distribution_menu, game_river_bet_menu,
                   game_showdown_menu, game_initialization_menu][round_number]


def get_user_command_string(command, player):  # возвращает строку для опции по номеру команды и по игроку
    get_string = lambda: ''
    if command == 0: get_string = lambda: f'Поднять <{game.CURRENT_MIN_BET - player.round_bet + 1} - {player.bank - 1}>'
    elif command == 1:
        if game.LAST_RAISER is None: get_string = lambda: f'Поднять {game.SAVABLE["GAME_MIN_BET"]}'
        else: get_string = lambda: f'Уравнять ({game.CURRENT_MIN_BET - player.round_bet})'
    elif command == 2: get_string = lambda: 'Пропустить'
    elif command == 3: get_string = lambda: f'Ва-банк ({player.bank})'
    elif command == 4: get_string = lambda: 'Сбросить'
    return get_string


def get_winners_string():
    winners = poker.Combination.get_winners([player for player in game.PLAYERS if not player.is_fold])
    winners_strings = [f'{winner.name} (+{poker.get_bank() // len(winners)}) - {get_combination_string(winner)}' for winner in winners]
    return ('\nПобедители: ' if len(winners) > 1 else '\nПобедитель: ') + '; '.join(winners_strings)


def get_command_string(command, player):  # возвращает строку комманды
    string = ''
    if command[0] == 0: string = f'Поднял {command[1]}'
    elif command[0] == 1:
        if player.get_index() == game.LAST_RAISER: string = f'Поднял {game.SAVABLE["GAME_MIN_BET"]}'
        else: string = f'Уравнял ({command[1]})'
    elif command[0] == 2: string = 'Пропустил'
    elif command[0] == 3: string = f'Ва-банк ({command[1]})'
    elif command[0] == 4: string = 'Сбросил'
    return string


def raise_command(*args):
    bet = int(args[0][1]) if args else (game.CURRENT_MIN_BET + 1 if game.CURRENT_MIN_BET > game.SAVABLE["GAME_MIN_BET"] else game.SAVABLE["GAME_MIN_BET"])
    game.PLAYERS[-1].do_command((0, bet), True)
    return get_round_menu(game.ROUND)()

def blind_command():
    if game.PLAYERS[-1].is_sb: game.PLAYERS[-1].do_command((0, game.SAVABLE["GAME_MIN_BET"]), True)
    if game.PLAYERS[-1].is_bb: game.PLAYERS[-1].do_command((0, game.SAVABLE["GAME_MIN_BET"] * 2), True)
    return get_round_menu(game.ROUND)()

def call_command():
    game.PLAYERS[-1].do_command((1, 0), True)
    return get_round_menu(game.ROUND)()

def check_command():
    game.PLAYERS[-1].do_command((2, 0), True)
    return get_round_menu(game.ROUND)()

def allin_command():
    game.PLAYERS[-1].do_command((3, 0), True)
    return get_round_menu(game.ROUND)()

def fold_command():
    game.PLAYERS[-1].do_command((4, 0), True)
    return get_round_menu(game.ROUND)()

def continue_command():
    poker.change_round()
    return get_round_menu(game.ROUND)()


def get_available_commands_options():  # возвращает список доступных команд в виде опций для пользователя
    user_commands = raise_command, call_command, check_command, allin_command, fold_command

    if game.IS_QUERY_ENDED or game.ROUND % 2 == 0:
        return ('Продолжить', continue_command), ('Пауза', game_pause_menu)
    elif game.ROUND % 2 == 1:
        if game.ROUND == 1 and game.PLAYERS[-1].round_bet == 0 and (game.PLAYERS[-1].is_sb or game.PLAYERS[-1].is_bb):
            if game.PLAYERS[-1].is_sb: return (f'Поднять {game.SAVABLE["GAME_MIN_BET"]}', blind_command), ('Пауза', game_pause_menu)
            if game.PLAYERS[-1].is_bb: return (f'Поднять {game.SAVABLE["GAME_MIN_BET"] * 2}', blind_command), ('Пауза', game_pause_menu)
        return [[get_user_command_string(command, game.PLAYERS[-1]), user_commands[command]] for command in poker.get_available_commands_number(game.PLAYERS[-1])] + [['Пауза', game_pause_menu]]


def get_cards_string(cards, hide=False):
    string = ''
    for card in cards:
        string += f'[{"XX" if hide else card.icon}] '
    return string


def get_combination_string(player):
    high_card = poker.Combination.sort_cards(player.combination[1], reverse=True)[0]
    second_card = poker.Combination.sort_cards(player.combination[1], reverse=True)[2] if player.combination[0] == 3 else None
    if player.combination[0] == 7:
        high_card = player.combination[1][0]
        second_card = player.combination[1][-1]
    kicker_card = poker.Combination.sort_cards(player.combination[2], reverse=True)[0] if len(player.combination[2]) > 0 else None
    if player.combination[0] == 9: return f'Стрит-флеш {high_card.icon}'
    if player.combination[0] == 8: return f'Каре {high_card.icon}, кикер {kicker_card.icon}'
    if player.combination[0] == 7: return f'Фул-хаус {high_card.icon} и {second_card.icon}'
    if player.combination[0] == 6: return f'Флеш {high_card.icon}'
    if player.combination[0] == 5: return f'Стрит {high_card.icon}'
    if player.combination[0] == 4: return f'Сет {high_card.icon}, кикер {kicker_card.icon}'
    if player.combination[0] == 3: return f'Две пары {high_card.icon} и {second_card.icon}, кикер {kicker_card.icon}'
    if player.combination[0] == 2: return f'Пара {high_card.icon}, кикер {kicker_card.icon}'
    if player.combination[0] == 1: return f'Старшая карта {player.combination[1][0].icon}'


def get_player_formatted_name(player):
    return format(player.name, ' <20')


def get_queue_string():
    queue = [game.PLAYERS[x] for x in game.INITIAL_QUEUE]
    string = ''
    for player in queue:
        cards = get_cards_string(player.get_cards(), (game.ROUND != 8) and (player.get_index() != game.SAVABLE["PLAYERS_NUMBER"] - 1))
        string += f'{get_player_formatted_name(player)}\t{player.get_role()}\t{player.bank} ф.\t{cards}'
        if player.is_fold: string += '\tСбросил'
        else:
            if game.ROUND == 8: string += f'\t{get_combination_string(player) if player.bank > 0 else get_combination_string(player)}'
            elif poker.get_player_allin_record(player): string += '\tВа-банк'
        string += '\n'
    return string + (get_winners_string() if game.ROUND == 8 else '')


def get_queue_commands_string():  # тоже, что и get_queue_string(), только каждая строка содержит команды, которые сделали игроки
    poker.start_query(False)
    queue = [(game.PLAYERS[record[1]], (record[2], record[3]), record[5]) for record in game.HISTORY_QUEUE if record[0] == (game.ROUND if game.ROUND % 2 == 1 else game.ROUND - 1) and record[4] == game.ROUND_STEP]
    string = ''
    for player, command, bank in queue:
        cards = get_cards_string(player.get_cards(), (game.ROUND == 8) or (player.get_index() != game.SAVABLE["PLAYERS_NUMBER"] - 1))
        string += f'{get_player_formatted_name(player)}\t{player.get_role()}\t{bank} ф.\t{cards}:\t{get_command_string(command, player)}\n'
    if not game.IS_QUERY_ENDED: string += f'{get_player_formatted_name(game.PLAYERS[-1])}\t{game.PLAYERS[-1].get_role()}\t{game.PLAYERS[-1].bank} ф.\t{get_cards_string(game.PLAYERS[-1].get_cards())}:\n'
    return string


def get_bots_mode_string():
    return {'passive': 'Пассивные', 'random': 'С произвольным поведением', 'trained': 'Обученные'}[
        game.SAVABLE["BOTS_MODE"]]


def main_menu():
    menu_list['main_menu'].print_menu()


def train_settings_menu():
    menu_list['train_settings_menu'].print_menu()


def game_settings_menu():
    File.save_settings(game, train_settings)
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


def train_initialization_menu():
    menu_list['train_initialization_menu'].print_menu()


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


def min_bank_menu():
    menu_list['min_bank_menu'].print_menu()


def bots_mode_menu():
    menu_list['bots_mode_menu'].print_menu()



def learning_bots_number_check(x):
    if not x.isdigit() or x == '':
        train_settings_menu()
        return True
    elif 1 <= int(x) <= 10:
        game.SAVABLE["PLAYERS_NUMBER"] = int(x)
        train_settings_menu()
        return True
    return False


def series_length_check(x):
    if not x.isdigit() or x == '':
        train_settings_menu()
        return True
    elif 1 <= int(x) <= 30:
        train_settings.SAVABLE["SERIES_LENGTH"] = int(x)
        train_settings_menu()
        return True
    return False


def series_number_check(x):
    if not x.isdigit() or x == '':
        train_settings_menu()
        return True
    elif 1 <= int(x) <= 10000000:
        train_settings.SAVABLE["SERIES_NUMBER"] = int(x)
        train_settings_menu()
        return True
    return False


def autosaves_frequency_check(x):
    if not x.isdigit() or x == '':
        train_settings_menu()
        return True
    elif 1 <= int(x) <= 120:
        train_settings.SAVABLE["AUTOSAVES_FREQUENCY"] = int(x)
        train_settings_menu()
        return True
    return False


def bots_number_check(x):
    if not x.isdigit() or x == '':
        game_settings_menu()
        return True
    elif 2 <= int(x) <= 10:
        game.SAVABLE["PLAYERS_NUMBER"] = int(x)
        game_settings_menu()
        return True
    return False


def bots_names_check(x):
    if x == '':
        game_settings_menu()
        return True
    game.SAVABLE["USR_BOTS_NAMES"] = ' '.join([name for name in x.split() if 2 <= len(name) <= 16])
    game_settings_menu()
    return False


def min_bet_check(x):
    if not x.isdigit() or x == '':
        game_settings_menu()
        return True
    elif 50 <= int(x) <= 1000000:
        game.SAVABLE["GAME_MIN_BET"] = int(x)
        game_settings_menu()
        return True
    return False


def rules_check(x):
    main_menu()
    return True


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


def main_check(x):
    game.GAME_WAS_INITIALIZED = False
    File.load_settings(game, train_settings)
    return True


def train_settings_check(x):
    return True


def game_settings_check(x):
    return True


def train_initialization_check(x):
    game.GAME_WITH_USER = False
    poker.set_game(reset_players=not game.GAME_WAS_INITIALIZED)
    game.GAME_WAS_INITIALIZED = True
    return True


def game_initialization_check(x):
    game.GAME_WITH_USER = True
    poker.set_game(reset_players=not game.GAME_WAS_INITIALIZED)
    game.GAME_WAS_INITIALIZED = True
    return True


def game_preflop_distribution_check(x):
    return True


def game_preflop_bet_check(x):
    return True


def game_flop_distribution_check(x):
    return True


def game_flop_bet_check(x):
    return True


def game_turn_distribution_check(x):
    return True


def game_turn_bet_check(x):
    return True


def game_river_distribution_check(x):
    return True


def game_river_bet_check(x):
    return True


def game_showdown_check(x):
    return True


def pause_rules_check(x):
    game_pause_menu()
    return True


def bots_mode_check(x):
    if int(x) == 1: game.SAVABLE["BOTS_MODE"] = 'passive'
    elif int(x) == 2: game.SAVABLE["BOTS_MODE"] = 'random'
    elif int(x) == 3: game.SAVABLE["BOTS_MODE"] = 'trained'
    game_settings_menu()
    return True


def min_bank_check(x):
    if x.isdigit() and 500 <= int(x) <= 10000000:
        game.SAVABLE["MIN_BANK"] = int(x)
        game_settings_menu()
        return True
    game_settings_menu()
    return False


menu_list = {
    # '': Menu('', [], TextInput('', lambda x: x)),
    'main_menu': Menu('Главное меню:', [
        ['Создать игру', game_initialization_menu],
        ['Создать тренировку', train_initialization_menu],
        ['Настройки игры', game_settings_menu],
        ['Правила игры', rules_menu],
        ['Завершение программы', exit]
    ], TextInput('Выберите номер команды: ', main_check)),

    'train_settings_menu': Menu('Настройки обучения:', [
        ['Длина серии игр', series_length_menu],
        ['Количество серий игр', series_number_menu],
        ['Частота автосохранений', autosaves_frequency_menu],
        ['Импорт базы данных', import_db_menu],
        ['Экспорт базы данных', export_db_menu],
        ['Вернуться в Настройки игры', game_settings_menu],
        ['Вернуться в Главное меню', main_menu]
    ], TextInput('Выберите номер команды: ', train_settings_check)),
    'learning_players_number_menu': Menu(lambda: f'Настройки обучения: Количество ботов - {game.SAVABLE["PLAYERS_NUMBER"]}', [], TextInput('Введите количество ботов (1-10): ', learning_bots_number_check)),
    'series_length_menu': Menu(lambda: f'Настройки обучения: Длина серии игр - {train_settings.SAVABLE["SERIES_LENGTH"]}', [], TextInput('Введите длину серии игр (1-30): ', series_length_check)),
    'series_number_menu': Menu(lambda: f'Настройки обучения: Количество серий игр - {train_settings.SAVABLE["SERIES_NUMBER"]}', [], TextInput('Введите количество обучающих серий (1-10000000): ', series_number_check)),
    'autosaves_frequency_menu': Menu(lambda: f'Настройки обучения: Частота автосохранений - {train_settings.SAVABLE["AUTOSAVES_FREQUENCY"]}', [], TextInput('Введите частоту автосохранений (до 120 минут): ', autosaves_frequency_check)),
    'import_db_menu': Menu(lambda: f'Настройки базы данных: Путь до последнего импортированного файла базы данных - {train_settings.SAVABLE["IMPORT_PATH"]}', [], TextInput('Введите путь до импортируемой базы данных: ', import_db_check)),
    'export_db_menu': Menu(lambda: f'Настройки базы данных: Путь до последнего экпортированного файла базы данных - {train_settings.SAVABLE["EXPORT_PATH"]}', [], TextInput('Введите путь сохранения базы данных: ', export_db_check)),

    'game_settings_menu': Menu('Настройки игры:', [
        ['Минимальная ставка', min_bet_menu],
        ['Минимальный банк игроков', min_bank_menu],
        ['Количество игроков', players_number_menu],
        ['Сложность ботов', bots_mode_menu],
        ['Имена ботов', bots_names_menu],
        ['Настройки обучения', train_settings_menu],
        ['Вернуться в Главное меню', main_menu]
    ], TextInput('Выберите номер команды: ', game_settings_check)),
    'players_number_menu': Menu(lambda: f'Настройки игры: Количество игроков - {game.SAVABLE["PLAYERS_NUMBER"]}', [], TextInput('Введите количество игроков (2-10): ', bots_number_check)),
    'min_bank_menu': Menu(lambda: f'Настройки игры: Минимальный банк игроков - {game.SAVABLE["MIN_BANK"]}', [], TextInput('Введите минимальный банк игроков (500-10000000): ', min_bank_check)),
    'bots_names_menu': Menu('Настройки игры: Имена ботов', [], TextInput('Введите новые имена ботов через пробел: ', bots_names_check)),
    'min_bet_menu': Menu(lambda: f'Настройки игры: Минимальная ставка - {game.SAVABLE["GAME_MIN_BET"]}', [], TextInput('Введите минимальную ставку (50-1000000): ', min_bet_check)),
    'rules_menu': Menu(lambda: f'Настройки игры: Правила игры - {train_settings.RULES}', [], TextInput('Введите Хоп-хей-ла-лей, чтобы продолжить: ', rules_check)),
    'bots_mode_menu': Menu(lambda: f'Настройки игры: Сложность ботов - {get_bots_mode_string()}', [
        ['Пассивные боты', game_settings_menu],
        ['Боты с произвольным поведением', game_settings_menu],
        ['Обученные боты', game_settings_menu]
    ], TextInput('Введите номер уровня сложности: ', bots_mode_check)),

    'train_initialization_menu': Menu(lambda: f'Инициализация тренировки\nКоличество игроков: {game.SAVABLE["PLAYERS_NUMBER"]}\nОбщее число игр: {train_settings.SAVABLE["SERIES_LENGTH"] * train_settings.SAVABLE["SERIES_NUMBER"]}\nЧастота автосохранений: {train_settings.SAVABLE["AUTOSAVES_FREQUENCY"]}', [
        ['Начать тренировку', get_round_menu(0)],
        ['Вернуться в Главное меню', main_menu],
    ], TextInput('Введите номер команды: ', train_initialization_check)),
    'game_initialization_menu': Menu(lambda: f'Инициализация игры\nКоличество игроков: {game.SAVABLE["PLAYERS_NUMBER"]}\nМинимальная ставка: {game.SAVABLE["GAME_MIN_BET"]}\nСложность ботов: {get_bots_mode_string()}', [
        ['Начать игру', get_round_menu(0)],
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
    'pause_rules_menu': Menu(lambda: f'Пауза: Правила игры - {train_settings.RULES}', [], TextInput('Введите Хоп-хей-ла-лей, чтобы продолжить: ', pause_rules_check)),
}




def start():
    main_menu()
