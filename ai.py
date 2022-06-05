import random
import numpy as np


def scale_cards(cards):
    ranks = list(get_ordinal_scaled_array([card.rank.level for card in cards], {level: level for level in range(1, 14)}))
    flushes = list(get_nominal_scaled_array([card.flush.name for card in cards], {'D', 'C', 'P', 'H'}))
    result = []
    for i in range(len(cards)):
        result += flushes[i] + [ranks[i]]
    return result


def scale_commands(commands):
    commands_types = get_nominal_scaled_array([command[0] for command in commands], {0, 1, 2, 3, 4})
    bets = [command[1] for command in commands]
    result = []
    for i in range(len(commands)):
        result += commands_types[i] + [bets[i]]
    return result


def get_minmax_scaled_array(array):  # шкалирование числовых данных
    array = np.array(array)
    return np.array(list(map(lambda x: (x - array.min()) / (array.max() - array.min()), array)))


def get_nominal_scaled_array(array, names_set):  # шкалирование категориальных номинальных данных
    array = np.array(array)
    return np.array([[name == item for name in names_set] for item in array])


def get_ordinal_scaled_array(array, names_dict):  # шкалирование категориальных порядковых данных
    array = np.array(array)
    return get_minmax_scaled_array(np.array([names_dict[item] for item in array]))


def scale_bank(chips, bank):
    return chips / bank - 1


class Brain:
    def __init__(self):
        self.weights = [None, None, None, None]
        self.gen_weights()

    def gen_weights(self):  # генерирует матрицы весов
        self.weights[0] = np.random.random((33, 10))  # вход к первому слою
        self.weights[1] = np.random.random((10, 10))  # первый слой к первому слою
        self.weights[2] = np.random.random((10, 10))  # первый слой к второму слою
        self.weights[3] = np.random.random((10, 7))  # второй слой к выходу

    def mutate_weights(self, uphold=False):  # после отбора среди победителей будут клоны и мутанты. Эта функция делает мутантов
        for matrix in self.weights:
            matrix *= random.random() / 100 + (uphold if uphold else round(random.random()))  # если uphold=True, то укрепляем веса, иначе или укрепляем, или ослабляем их

    @staticmethod
    def activate(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def get_output(input_layer, weights):  # возращает активированное произведение весов на текущие значения нейронов
        return Brain.activate(np.dot(weights, input_layer))

    def get_command(self, players, min_bet, bank, self_player, common_cards, available_commands):
        input_layer = [scale_bank(min_bet, self_player.bank), scale_bank(bank, self_player.bank)] +\
                      [scale_bank(player.bank, self_player.bank) for player in players] +\
                      scale_cards(self_player.get_cards()) + scale_cards(common_cards) + [0 for _ in range((5 - len(common_cards)) * 5)] +\
                      scale_commands([player.last_command for player in players]) + [0 for _ in range((10 - len(players)) * 6)]

        output1 = Brain.get_output(Brain.activate(np.array(input_layer)), self.weights[0])
        output2 = Brain.get_output(output1, self.weights[1])
        output2 = Brain.get_output(output2, self.weights[2])
        output = Brain.get_output(output2, self.weights[3])
        # available_commands = [0 - поднять, 1 - уравнять, 2 - пропустить, 3 - ва-банк, 4 - сбросить]
        # output = [поднять минимум, уравнять, пропустить, ва-банк, сбросить, поднять два минимума, поднять три минимума]
        # присваиваем каждому выходу свою команду, фильтруем их по наличию в списке доступных команд, сортируем по убыванию, берем первый элемент
        command = sorted(filter(lambda _: _[1] in available_commands, [(output[i], i) for i in range(5)] + [(output[5], 0), (output[6], 0)]), key=lambda _: _[0], reverse=True)[0]
        if command[0] == 0: return 0, min_bet
        if command[0] == 5: return 0, min_bet * 2
        if command[0] == 6: return 0, min_bet * 3
        return command[1], 0
