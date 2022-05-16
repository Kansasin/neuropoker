import random
import config
import game_settings as game


class Player:
    def __init__(self, name):
        self.name = name
        self.bank = game.DEFAULT_BANK
        self.is_fold = False
        self.last_command = tuple([-1, 0])  # команда -1 означает, что команда отсутствует
        self.round_bet = 0  # ставка, которую игрок поставил в течение раунда
        self.is_bb = False
        self.is_sb = False

    def get_index(self): #  использовать только после настройки игры
        return game.PLAYERS.index(self)

    def get_queue_index(self, start=0):
        return game.INITIAL_QUEUE.index(self.get_index(), start)

    def get_cards(self):
        return [game.CARDS[self.get_index() * 2], game.CARDS[self.get_index() * 2 + 1]]

    def transfer_chips(self, amount, is_bank_to_player=False):
        if is_bank_to_player:  # если банк отправляет фишки игроку (например, в случае победы или ввода чит-кода пользователем), то перечисляем с банка на счет игрока
            self.bank += amount
            game.BANK -= amount
        elif amount - self.bank <= 0:  # иначе, если у игрока достаточно фишек, то он отправляет нужное количество
            game.BANK += amount
            self.bank -= amount
        elif amount - self.bank > 0:  # иначе, если фишек не хватает, то отправляет то, что есть
            game.BANK += self.bank
            self.bank = 0

    def exec_command(self, command, bet):
        if command == 0:  # поднять
            game.LAST_RAISER = self.get_index()
            game.CURRENT_MIN_BET = self.round_bet + bet
            shift_queue(game.LAST_RAISER)
            self.transfer_chips(bet)
        elif command == 1:  # уравнять
            bet = game.CURRENT_MIN_BET - self.round_bet
            self.transfer_chips(bet)
        elif command == 2:  # пропустить
            bet = 0
        elif command == 3:  # ва-банк
            bet = self.bank
            if self.bank > game.CURRENT_MIN_BET:  # ва-банк, если это не вынужденное решение
                game.LAST_RAISER = self.get_index()
                game.CURRENT_MIN_BET = self.round_bet + bet
                shift_queue(game.LAST_RAISER)
            self.transfer_chips(bet)
            if game.INITIAL_QUEUE.index(self.get_index()):  # если игрок еще в очереди, то убрать его оттуда
                game.INITIAL_QUEUE.pop(game.INITIAL_QUEUE.index(self.get_index()))
                game.CURRENT_QUEUE.pop(game.CURRENT_QUEUE.index(self.get_index()))
        elif command == 4:  # сбросить
            bet = 0
            self.is_fold = True
            if game.INITIAL_QUEUE.index(self.get_index()):  # если игрок еще в очереди, то убрать его оттуда
                game.INITIAL_QUEUE.pop(game.INITIAL_QUEUE.index(self.get_index()))
                game.CURRENT_QUEUE.pop(game.CURRENT_QUEUE.index(self.get_index()))
        self.last_command = command, bet
        self.round_bet += bet
        update_history(self.get_index(), self.last_command)
        print(self.last_command, self.round_bet, self.name)
        print(game.HISTORY_QUEUE)
        print(game.CURRENT_MIN_BET, game.LAST_RAISER, game.CURRENT_QUEUE)
        breakpoint()

    def get_command(self, do_random=True):  # возвращает кортеж из номера команды и размера ставки исходя из списка доступных команд
        available_commands = get_available_commands_number(self)
        print(available_commands)
        if do_random:
            command = available_commands[random.randint(0, len(available_commands) - 1)]
            min_bet = (game.CURRENT_MIN_BET + 1 if game.CURRENT_MIN_BET > game.GAME_MIN_BET else game.GAME_MIN_BET) - self.round_bet
            bet = random.randint(min_bet, self.bank - 1) if command == 0 else 0
        else:
            command = available_commands[0] if available_commands[0] != 0 else available_commands[1]
            bet = game.GAME_MIN_BET if command == 0 else 0
        if game.ROUND <= 1 and self.round_bet == 0:  # если сейчас ставки на префлопе, и игрок не делал ставок, то
            if self.get_queue_index() == 0:  # если игрок - м.блайнд, то обязательно ставим минимальную ставку
                command = 0
                bet = game.GAME_MIN_BET
            elif self.get_queue_index() == 1:  # а если б.блайнд, то двойную минимальную ставку
                command = 0
                bet = game.GAME_MIN_BET * 2
        self.exec_command(command, bet)
        return command, bet


class Bot(Player):
    def __init__(self, name):
        super().__init__(name)
        self.is_user = False


class User(Player):
    def __init__(self, name):
        super().__init__(name)
        self.is_user = True


shuffle_players = lambda players: random.shuffle(players)  # перемешать игроков

def query_players():  # функция опрашивает каждого не сбросившего игрока с фишками (без пользователя)
    reset_last_commands(False)
    for player in [game.PLAYERS[x] for x in game.CURRENT_QUEUE]:
        player.get_command()

def query_players_with_user(start_from_user=False):  # опрос игроков проводится сначала до пользователя, а затем от него, не включая самого пользователя, т. к. он опрашивается отдельно
    user_is_reached = False
    for player in [game.PLAYERS[x] for x in game.CURRENT_QUEUE]:
        if player.is_user:
            user_is_reached = True
            continue
        if start_from_user and user_is_reached:
            reset_last_commands(False)
            player.get_command()
        if not start_from_user and not user_is_reached:
            player.get_command()

def set_queue(players):  # настроить очередь
    game.PLAYERS = players
    game.INITIAL_QUEUE = [i for i in range(game.PLAYERS_NUMBER)]
    random.shuffle(game.INITIAL_QUEUE)
    game.PLAYERS[game.INITIAL_QUEUE[0]].is_sb = True
    game.PLAYERS[game.INITIAL_QUEUE[1]].is_bb = True
    game.CURRENT_QUEUE = game.INITIAL_QUEUE[:]

def shift_queue(index):  # те пользователи, что стояли до указанного индекса, переходят в конец очереди, и удаляются из ее начала
    game.CURRENT_QUEUE = game.CURRENT_QUEUE[index:] + game.CURRENT_QUEUE[:index]

def update_history(index, command):
    game.HISTORY_QUEUE.append((game.ROUND, index, command[0], command[1]))

def reset_last_commands(reset_round_bet=True):
    for player in game.PLAYERS:
        player.last_command = -1, 0
        if reset_round_bet: player.round_bet = 0

def reset_round():
    game.CURRENT_QUEUE = [i for i in game.INITIAL_QUEUE if game.PLAYERS[i].bank > 0 and not game.PLAYERS[i].is_fold]
    game.CURRENT_MIN_BET = game.GAME_MIN_BET
    game.LAST_RAISER = 0

    reset_last_commands()

def get_bank():
    return sum([record[3] for record in game.HISTORY_QUEUE])



class Flush:
    def __init__(self, name):
        self.color = 'black' if name in ['P', 'C'] else 'red'
        self.icon = '♦' if name == 'D' else '♣' if name == 'C' else '♠' if name == 'P' else '♥' if name == 'H' else ''
        self.name = name


flushes = [Flush('D'), Flush('C'), Flush('P'), Flush('H')]


class Rank:
    def __init__(self, level):  # A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
        self.level = level
        self.icon = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'][int(level) - 1]
        self.is_ace = level == 1


ranks = [Rank(1), Rank(2), Rank(3), Rank(4), Rank(5), Rank(6), Rank(7), Rank(8), Rank(9), Rank(10), Rank(11), Rank(12),
         Rank(13)]


class Card:
    def __init__(self, rank, flush):
        self.rank = rank
        self.flush = flush
        self.icon = rank.icon + flush.name


shuffle_cards = lambda cards: random.shuffle(cards)  # перемешать карты


def set_cards(cards):
    game.CARDS = cards[:26]

def get_table_cards():
    if game.ROUND in [2, 3]:
        return game.CARDS[20:23]
    elif game.ROUND in [4, 5]:
        return game.CARDS[20:24]
    elif game.ROUND in [6, 7, 8]:
        return game.CARDS[20:25]
    else:
        return []


def set_game():
    reset_round()
    game.BANK = 0

    names = config.BOTS_NAMES.split(' ')  # берем все доступные имена
    if config.USER_BOTS_NAMES != '': names += config.USER_BOTS_NAMES.split(' ')  # если есть пользовательские имена, то добавляем их в список
    random.shuffle(names)  # перемешиваем имена
    players = [Bot(f'BOT_{names[i]}') for i in range(game.PLAYERS_NUMBER - 1)]  # создаем список игроков из ботов
    cards = [Card(rank, flush) for rank in ranks for flush in flushes]  # создаем колоду
    shuffle_cards(cards)  # перемешиваем колоду
    set_cards(cards)  # настраиваем карты в конфигах
    shuffle_players(players)  # перемешиваем игроков
    players += [User('USR_User')]  # добавляем в список игроков пользователя, если игра с пользователем
    set_queue(players)  # настраиваем игроков и очередь в конфигах


def is_bets_equal():
    bets = [player.round_bet for player in game.PLAYERS if player.get_index() in game.CURRENT_QUEUE]
    return all([bets[0] == bet for bet in bets])


def get_available_commands_number(player):  # возвращает список номеров доступных команд для указанного игрока
    if player.is_fold: return [2]  # если уже сбросили, то можно лишь пропустить
    commands = []
    if player.bank > game.CURRENT_MIN_BET - player.round_bet: commands += [0]
    if player.bank > game.CURRENT_MIN_BET - player.round_bet > 0 and game.CURRENT_MIN_BET != game.GAME_MIN_BET: commands += [1]
    if game.CURRENT_MIN_BET - player.round_bet == 0 or is_bets_equal() or player.bank == 0: commands += [2]
    if player.bank > 0: commands += [3]
    return commands + [4]
