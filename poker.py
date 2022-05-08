import random
import config
import game_settings as game


class Player:
    def __init__(self, name):
        self.name = name
        self.bank = game.DEFAULT_BANK
        self.is_fold = False

    def get_index(self): #  использовать только после настройки игры
        return game.PLAYERS.index(self)

    def get_queue_index(self):
        return game.CURRENT_QUEUE.index(self.get_index())

    def get_cards(self):
        return [game.CARDS[self.get_index() * 2], game.CARDS[self.get_index() * 2 + 1]]


class Bot(Player):
    def __init__(self, name):
        super().__init__(name)


class User(Player):
    def __init__(self, name):
        super().__init__(name)


shuffle_players = lambda players: random.shuffle(players)  # перемешать игроков


def set_queue(players):  # настроить очередь
    game.PLAYERS = players
    game.INITIAL_QUEUE = [i for i in range(game.PLAYERS_NUMBER)]
    random.shuffle(game.INITIAL_QUEUE)
    game.CURRENT_QUEUE = game.INITIAL_QUEUE[:]
    random.shuffle(game.INITIAL_QUEUE)

def shift_queue(index):
    game.CURRENT_QUEUE = game.INITIAL_QUEUE[index:] + game.INITIAL_QUEUE[:index]


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