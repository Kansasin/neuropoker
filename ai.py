import random
import numpy as np
import game_settings


def scale_cards(cards):
    pass


def get_minmax_scaled_array(array):  # шкалирование числовых данных
    return np.array(list(map(lambda x: (x - array.min()) / (array.max() - array.min()), array)))


def get_nominal_scaled_array(array):  # шкалирование категориальных номинальных данных
    pass


def get_ordinal_scaled_array(array):  # шкалирование категориальных порядковых данных
    pass


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
    def get_output(input_layer, weights):  # возращает активированное произведение весов на текущие значения нейронов
        return 1 / (1 + np.exp(-np.dot(weights, input_layer)))

    def get_command(self, players, min_bet, bank, self_player, common_cards, available_commands):
        input_layer = []  # TODO: шкалировать данные, чтобы отправлять их в нейросеть
        output1 = Brain.get_output(input_layer, self.weights[0])
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
