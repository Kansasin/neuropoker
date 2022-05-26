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
        self.combination = 0, [], []

    def get_role(self):
        if self.is_sb: return "м. блайнд"
        if self.is_bb: return "б. блайнд"
        return "игрок\t"

    def get_index(self): #  использовать только после настройки игры
        return game.PLAYERS.index(self)

    def get_queue_index(self, start=0):
        return game.INITIAL_QUEUE.index(self.get_index(), start)

    def get_next_player(self):
        next_player = game.PLAYERS[game.INITIAL_QUEUE[(self.get_queue_index() + 1) % game.PLAYERS_NUMBER]]
        if do_all_command() and is_bets_equal():
            # print(*[(player.name, player.is_fold, player.get_queue_index(), player.round_bet, player.last_command[0]) for player in game.PLAYERS], sep="\n")
            game.IS_QUERY_ENDED = True
            # next_player = game.PLAYERS[-1]
        # print(self.name, next_player.name, game.INITIAL_QUEUE, do_all_command(), is_bets_equal())
        # breakpoint()
        return next_player

    def get_cards(self):
        return [game.CARDS[self.get_index() * 2], game.CARDS[self.get_index() * 2 + 1]]

    def get_bank(self):
        for record in game.HISTORY_QUEUE:
            if record[0] != game.ROUND: continue
            return record[4]
        return self.bank

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
            game.ROUND_STEP += 1
        elif command == 1:  # уравнять
            bet = game.CURRENT_MIN_BET - self.round_bet
        elif command == 2:  # пропустить
            bet = 0
        elif command == 3:  # ва-банк
            bet = self.bank
            if self.bank > game.CURRENT_MIN_BET - self.round_bet:  # если по всем признакам ва-банк == рейз
                game.LAST_RAISER = self.get_index()
                game.CURRENT_MIN_BET = self.round_bet + bet
                game.ROUND_STEP += 1
        elif command == 4:  # сбросить
            bet = 0
            self.is_fold = True
        self.transfer_chips(bet)
        self.last_command = command, bet
        self.round_bet += bet
        update_history(self.get_index(), self.last_command)


        # get_command_string = lambda num: 'поднял' if num == 0 else ('уравнял' if num == 1 else ('пропустил' if num == 2 else ('ва-банк' if num == 3 else ('сбросил' if num == 4 else ''))))
        # print(f'{self.name} {get_command_string(self.last_command[0])} {self.last_command[1]} ф.')
        # print(*[(record[0], game.PLAYERS[record[1]].name, get_command_string(record[2]), f'{record[3]} ф.', f'на шаге {record[4]} осталось {record[5]} ф.') for record in game.HISTORY_QUEUE], sep="\n")
        # if not game.LAST_RAISER is None: print(f'Последний поднял {game.PLAYERS[game.LAST_RAISER].name} - {game.PLAYERS[game.LAST_RAISER].round_bet} ф.')
        # else: print(f'Никто не поднял еще, минимальная ставка {game.CURRENT_MIN_BET} ф.')
        # breakpoint()

    def get_combination(self):
        self.combination = Combination.get_combination_level(self.get_cards() + game.CARDS[-5:])
        # print(self.name)
        # print([card.icon for card in self.get_cards()], [card.icon for card in game.CARDS[-5:]])
        # print(self.combination[0], [card.icon for card in self.combination[1]], [card.icon for card in self.combination[2]], sep="\n")
        # breakpoint()
        return self.combination


class Bot(Player):
    def __init__(self, name):
        super().__init__(name)
        self.is_user = False

    def do_command(self, do_random=True):  # возвращает кортеж из номера команды и размера ставки исходя из списка доступных команд
        if self.is_fold or self.bank <= 0 or game.IS_QUERY_ENDED: return
        available_commands = get_available_commands_number(self)
        # print(self.name, available_commands)
        # breakpoint()
        if do_random:
            command = available_commands[random.randint(0, len(available_commands) - 1)]
            min_bet = (game.CURRENT_MIN_BET + 1 if game.CURRENT_MIN_BET > game.GAME_MIN_BET else game.GAME_MIN_BET) - self.round_bet
            bet = random.randint(min_bet, self.bank - 1) if command == 0 else 0
        else:
            command = 4
            if 2 in available_commands: command = 2
            elif 1 in available_commands: command = 1
            elif 3 in available_commands: command = 3
            bet = game.GAME_MIN_BET if command == 0 else 0
        if game.ROUND <= 1 and self.round_bet == 0:  # если сейчас ставки на префлопе, и игрок не делал ставок, то
            if self.is_sb:  # если игрок - м.блайнд, то обязательно ставим минимальную ставку
                command = 0
                bet = game.GAME_MIN_BET
            elif self.is_bb:  # а если б.блайнд, то двойную минимальную ставку
                command = 0
                bet = game.GAME_MIN_BET * 2
        self.exec_command(command, bet)


class User(Player):
    def __init__(self, name):
        super().__init__(name)
        self.is_user = True

    def do_command(self, command=(-1, 0), user_ready=False):
        if user_ready:
            self.exec_command(*command)
            start_query(start_from_user=True)


shuffle_players = lambda players: random.shuffle(players)  # перемешать игроков


def start_query(start_from_user=False):  # стартуем опрос игроков от начала или от пользователя, если надо было прерваться на получение его ввода
    player = game.PLAYERS[-1].get_next_player() if start_from_user else game.PLAYERS[game.INITIAL_QUEUE[0]]
    while not game.IS_QUERY_ENDED and not player.is_user:
        player.do_command(do_random=False)
        player = player.get_next_player()
    if game.IS_QUERY_ENDED:
        if start_from_user: return
        if not game.GAME_WITH_USER: change_round()


def set_queue(players, reset_players=False):  # настроить очередь
    if reset_players:
        game.PLAYERS = players
        game.INITIAL_QUEUE = [i for i in range(game.PLAYERS_NUMBER)]
    random.shuffle(game.INITIAL_QUEUE)
    game.HISTORY_QUEUE = []
    for player in game.PLAYERS:
        player.is_bb = player.is_sb = player.is_fold = False
        player.last_command = -1, 0
        player.round_bet = 0
        player.get_combination()
        if player.bank < game.DEFAULT_BANK: player.bank = game.DEFAULT_BANK
    game.PLAYERS[game.INITIAL_QUEUE[0]].is_sb = game.PLAYERS[game.INITIAL_QUEUE[1]].is_bb = True


def update_history(index, command):
    game.HISTORY_QUEUE.append((game.ROUND, index, command[0], command[1], game.ROUND_STEP, game.PLAYERS[index].bank))


def reset_last_commands(reset_round_bet=True):
    for player in game.PLAYERS:
        player.last_command = -1, 0
        if reset_round_bet: player.round_bet = 0


def change_round(round_number=None):
    if not (round_number is None): game.ROUND = round_number
    else:
        game.ROUND = (game.ROUND + 1) % 9 if is_bets_equal() else game.ROUND
        if players_alive() <= 1 and game.IS_QUERY_ENDED: game.ROUND = 8
        if game.ROUND == 8: split_bank()
        reset_round()


def reset_round():
    game.CURRENT_MIN_BET = game.GAME_MIN_BET
    game.LAST_RAISER = None
    game.IS_QUERY_ENDED = False
    game.ROUND_STEP = 0

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
    def __init__(self, level):  # 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A
        self.level = level
        self.icon = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'][int(level) - 1]
        self.is_ace = level == 1


ranks = [Rank(1), Rank(2), Rank(3), Rank(4), Rank(5), Rank(6), Rank(7), Rank(8), Rank(9), Rank(10), Rank(11), Rank(12),
         Rank(13)]


class Card:
    def __init__(self, rank, flush):
        self.rank = rank
        self.flush = flush
        self.icon = rank.icon + flush.icon


shuffle_cards = lambda cards: random.shuffle(cards)  # перемешать карты



def get_table_cards():
    if game.ROUND in [2, 3]:
        return game.CARDS[-5:-2]
    elif game.ROUND in [4, 5]:
        return game.CARDS[-5:-1]
    elif game.ROUND in [6, 7, 8]:
        return game.CARDS[-5:]
    else:
        return []


def set_game(reset_players=True):
    reset_round()
    game.BANK = 0
    game.ROUND = 0

    cards = [Card(rank, flush) for rank in ranks for flush in flushes]  # создаем колоду
    shuffle_cards(cards)  # перемешиваем колоду
    game.CARDS = cards[:26]  # настраиваем карты в конфигах

    players = game.PLAYERS
    if reset_players:
        names = config.BOTS_NAMES.split(' ')  # берем все доступные имена
        random.shuffle(names)  # перемешиваем имена
        if config.USER_BOTS_NAMES != '':  # если пользователь задал имена, то они используются в первую очередь
            user_names = config.USER_BOTS_NAMES.split()
            random.shuffle(user_names)
            names = user_names + names
        players = [Bot(f'BOT_{names[i]}') for i in range(game.PLAYERS_NUMBER - 1)]  # создаем список игроков из ботов
        shuffle_players(players)  # перемешиваем игроков
        players += [User('USR_User')]  # добавляем в список игроков пользователя, если игра с пользователем
    set_queue(players, reset_players)  # настраиваем игроков и очередь в конфигах


def split_bank():
    winners = Combination.get_winners([player for player in game.PLAYERS if not player.is_fold])
    # print([winner.name for winner in winners], [player.name for player in game.PLAYERS if not player.is_fold])
    # breakpoint()
    for winner in winners:
        if winner not in winners or winner.is_fold: continue
        winner.transfer_chips(game.BANK // len(winners), is_bank_to_player=True)


def do_all_command():  # все ли выбрали команду
    return all([player.last_command[0] != -1 for player in game.PLAYERS if not player.is_fold and player.bank > 0])


def do_any_command():  # кто-нибудь выбрал команду
    return any([player.last_command[0] != -1 for player in game.PLAYERS if not player.is_fold and player.bank > 0])


def players_alive():  # сколько игроков все еще играет (кто не фолданул и с фишками)
    return len([player for player in game.PLAYERS if not player.is_fold and player.bank > 0])


def get_player_allin_record(player):
    for record in game.HISTORY_QUEUE:
        if record[1] != player.get_index(): continue
        if record[2] == 3: return record
    return None


def is_bets_equal():  # сравнивает ставки тех игроков, кто в этом раунде ставил и не фолданул, и если ставки равны, то возвращает True
    bets = [player.round_bet for player in game.PLAYERS if not player.is_fold and (player.round_bet != 0 or player.bank != 0)]
    return all([bets[0] == bet for bet in bets])


def is_bets_zero():
    return all([player.round_bet == 0 for player in game.PLAYERS if not player.is_fold and player.bank > 0])


def get_available_commands_number(player):  # возвращает список номеров доступных команд для указанного игрока
    if player.is_fold: return [2]  # если уже сбросили, то можно лишь пропустить
    if player.bank == 0: return [2]  # если у пользователя нет фишек, то может только сбросить и пропустить
    commands = []
    if player.bank > game.CURRENT_MIN_BET - player.round_bet + 1 > 0: commands += [0]
    if player.bank > game.CURRENT_MIN_BET - player.round_bet > 0: commands += [1]
    if is_bets_equal(): commands += [2]
    if player.bank > 0: commands += [3]
    return commands + [4]




class Combination:
    @staticmethod
    def test(test_name='get_combo'):
        if test_name == 'get_combo':
            cards = [Card(rank, flush) for rank in ranks for flush in flushes]
            shuffle_cards(cards)
            print([card.icon for card in cards[:7]])
            combination = Combination.get_combination_level(cards[:7])
            print(combination[0])
            print([card.icon for card in combination[1]])
            print([card.icon for card in combination[2]])
            while input("any symbol to end, enter to continue... ") == '':
                shuffle_cards(cards)
                print([card.icon for card in cards[:7]])
                combination = Combination.get_combination_level(cards[:7])
                print(combination[0])
                print([card.icon for card in combination[1]])
                print([card.icon for card in combination[2]])
        elif test_name == 'statistic':
            num = 1000000
            count = {i + 1: 0 for i in range(9)}
            cards = [Card(rank, flush) for rank in ranks for flush in flushes]
            for i in range(num):
                shuffle_cards(cards)
                combination = Combination.get_combination_level(cards[:7])
                count[combination[0]] += 1
            print({i: format(stat / num * 100, '.2f') + '%' for i, stat in count.items()})
        elif test_name == 'winner':
            cards = [Card(rank, flush) for rank in ranks for flush in flushes]
            shuffle_cards(cards)
            combination1 = Combination.get_combination_level(cards[:7])
            combination2 = Combination.get_combination_level(cards[2:9])
            print([card.icon for card in cards[2:7]])
            print([card.icon for card in cards[0:2]])
            print([card.icon for card in cards[7:9]], end="\n\n")
            print(combination1[0], [card.icon for card in combination1[1]], [card.icon for card in combination1[2]], end="\n\n")
            print(combination2[0], [card.icon for card in combination2[1]], [card.icon for card in combination2[2]], end="\n\n")
            if combination1[0] == combination2[0]:
                comparison = Combination.compare_cards(combination1[1], combination2[1]), Combination.compare_cards(combination1[2], combination2[2])
            else:
                comparison = [0] if combination1[0] > combination2[0] else [1]
            print(comparison)

            while input("any symbol to end, enter to continue... ") == '':
                shuffle_cards(cards)
                combination1 = Combination.get_combination_level(cards[:7])
                combination2 = Combination.get_combination_level(cards[2:9])
                print([card.icon for card in cards[2:7]])
                print([card.icon for card in cards[0:2]])
                print([card.icon for card in cards[7:9]], end="\n\n")
                print(combination1[0], [card.icon for card in combination1[1]], [card.icon for card in combination1[2]], end="\n\n")
                print(combination2[0], [card.icon for card in combination2[1]], [card.icon for card in combination2[2]], end="\n\n")
                if combination1[0] == combination2[0]:
                    comparison = Combination.compare_cards(combination1[1], combination2[1]), Combination.compare_cards(combination1[2], combination2[2])
                else:
                    comparison = [0] if combination1[0] > combination2[0] else [1]
                print(comparison)


    @staticmethod
    def compare_cards(cards1, cards2):  # сравнивает два списка карт, возвращает индекс одного из них, где карты сильнее, либо индексы обоих, если карты равны
        if len(cards1) == 0 or len(cards2) == 0: return [0, 1]
        Combination.sort_cards(cards1)
        Combination.sort_cards(cards2)
        for i in range(len(cards1)):
            if cards1[i].rank.level > cards2[i].rank.level: return [0]
            if cards2[i].rank.level > cards1[i].rank.level: return [1]
        return [0, 1]
    @staticmethod
    def get_winners(players):
        winners = [players[0]]
        for player in players:
            if player == winners[0]: continue
            if player.combination[0] == winners[0].combination[0]:
                high_card_comparison = Combination.compare_cards(player.combination[1], winners[0].combination[1])
                if len(high_card_comparison) == 2:
                    kicker_card_comparison = Combination.compare_cards(player.combination[2], winners[0].combination[2])
                    if len(kicker_card_comparison) == 2: winners.append(player)
                    elif kicker_card_comparison[0] == 0: winners = [player]
                elif high_card_comparison[0] == 0: winners = [player]
            elif player.combination[0] > winners[0].combination[0]: winners = [player]
        return winners
    @staticmethod
    def get_combination_level(cards):  # возвращает кортеж из уровня комбинации, уровня старшей карты комбинации (и вторая старшая карта комбинации, если комбинация фулхаус или две пары) и уровня кикера, если он есть (если нет, то кикер = None)
        methods = [Combination.get_straight_flush, Combination.get_quads, Combination.get_full_house,
                   Combination.get_flush, Combination.get_straight, Combination.get_set,
                   Combination.get_two_pairs, Combination.get_pair, Combination.get_high_card]
        for method in methods:
            combination_cards = method(cards)  # фулхаус и две пары возвращают кортеж из двух списков карт, если комбинация собралась, иначе пустой список, остальные просто список карт
            if len(combination_cards) == 0: continue
            combination_cards_row = (combination_cards[0] + combination_cards[1]) if method in [methods[2], methods[6]] else combination_cards  # если возвращен кортеж, то склеиваем в один список, иначе просто приравниваем к списку
            kickers = Combination.sort_cards([card for card in cards if card not in combination_cards_row], reverse=True)[:5 - len(combination_cards_row)]
            level = [0, combination_cards, kickers]
            if method == methods[0] and len(combination_cards) == 5: level[0] = 9
            elif method == methods[1] and len(combination_cards) == 4: level[0] = 8
            elif method == methods[2] and len(combination_cards_row) == 5: level[0], level[1] = 7, combination_cards_row
            elif method == methods[3] and len(combination_cards) == 5: level[0] = 6
            elif method == methods[4] and len(combination_cards) == 5: level[0] = 5
            elif method == methods[5] and len(combination_cards) == 3: level[0] = 4
            elif method == methods[6] and len(combination_cards_row) == 4: level[0], level[1] = 3, combination_cards_row
            elif method == methods[7] and len(combination_cards) == 2: level[0] = 2
            elif method == methods[8]: level[0] = 1
            if level[0] != 0: return level[0], Combination.sort_cards(level[1], reverse=True), Combination.sort_cards(level[2], reverse=True)
        return 0, [], []
    @staticmethod
    def sort_cards(cards, reverse=False):
        cards.sort(key=lambda _: _.flush.name, reverse=reverse)
        cards.sort(key=lambda _: _.rank.level, reverse=reverse)
        return cards
    @staticmethod
    def get_high_card(cards):
        Combination.sort_cards(cards, reverse=True)
        return [cards[0]]
    @staticmethod
    def get_duplicates(cards):
        Combination.sort_cards(cards)  # отсортированы по возрастанию (2,3...Q,K,A)
        duplicates = dict()
        for card in cards:
            if card.rank.level in duplicates: duplicates[card.rank.level].append(card)
            else: duplicates[card.rank.level] = [card]
        return duplicates
    @staticmethod
    def get_straight(cards, return_duplicates=False):
        if len(cards) < 5: return []
        duplicates = list(Combination.get_duplicates(cards).values())
        duplicates.reverse()
        straight = [duplicates[0]]
        for i in range(len(duplicates) - 1):
            duplicate1 = duplicates[i]
            duplicate2 = duplicates[i + 1]
            if duplicate1[0].rank.level == duplicate2[0].rank.level + 1: straight.append(duplicate2)
            else: straight = [duplicate2]
            if len(straight) >= 5: break
        if len(straight) < 5: return []
        return straight[-5:] if return_duplicates else [duplicate[0] for duplicate in straight[-5:]]
    @staticmethod
    def get_flush(cards):
        if len(cards) < 5: return []
        Combination.sort_cards(cards, reverse=True)
        duplicates = dict()
        for card in cards:
            if card.flush.name in duplicates: duplicates[card.flush.name].append(card)
            else: duplicates[card.flush.name] = [card]
        highest = None
        for duplicate in duplicates.values():
            if highest is None and len(duplicate) >= 5: highest = duplicate
            elif len(duplicate) >= 5 and Combination.get_high_card(duplicate)[0].rank.level > Combination.get_high_card(highest)[0].rank.level:
                highest = duplicate
        return highest[:5] if not highest is None else []
    @staticmethod
    def get_straight_flush(cards):
        return Combination.get_flush(Combination.get_straight(cards))
    @staticmethod
    def get_pair(cards):
        result = [card_list for card_list in Combination.get_duplicates(cards).values() if len(card_list) == 2]
        return result[-1] if len(result) > 0 else []
    @staticmethod
    def get_two_pairs(cards):
        result = [card_list for card_list in Combination.get_duplicates(cards).values() if len(card_list) == 2]
        return result[-2:][::-1] if len(result) >= 2 else []
    @staticmethod
    def get_set(cards):
        result = [card_list for card_list in Combination.get_duplicates(cards).values() if len(card_list) == 3]
        return result[-1] if len(result) > 0 else []
    @staticmethod
    def get_quads(cards):
        result = [card_list for card_list in Combination.get_duplicates(cards).values() if len(card_list) == 4]
        return result[-1] if len(result) > 0 else []
    @staticmethod
    def get_full_house(cards):  # старшинство определяется сначала по сету, потом по паре
        result = Combination.get_set(cards), Combination.get_pair(cards)
        return result if len(result[0] + result[1]) == 5 else []

if __name__ == '__main__':
    Combination.test('statistic')