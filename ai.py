import random
import numpy as np
import game_settings


def vectorize_cards(cards):
    ranks = [card.rank.level for card in cards]
    flushes = [card.flush.name for card in cards]
    return ranks, flushes


class Brain:
    def __init__(self):
        self.weights = [None, None, None]

    def gen_weights(self):  # генерирует матрицы весов
        self.weights[0] = np.random.random((33, 10))  # вход к первому слою
        self.weights[1] = np.random.random((10, 10))  # первый слой к первому слою
        self.weights[2] = np.random.random((10, 10))  # первый слой к второму слою
        self.weights[3] = np.random.random((10, 2))  # второй слой к выходу

    def mutate_weights(self):  # после отбора среди победителей будут клоны и мутанты. Эта функция делает мутантов
        for matrix in self.weights:
            matrix *= random.random() / 100

    @staticmethod
    def get_output(input_layer, weights):  # возращает активированное произведение весов на текущие значения нейронов
        return 1 / (1 + np.exp(-np.dot(weights, input_layer)))

    def get_command(self, players, min_bet, bank, self_player, common_cards, available_commands):
        input_layer = []  # TODO: шкалировать данные, чтобы отправлять их в нейросеть
        output1 = Brain.get_output(input_layer, self.weights[0])
        output2 = Brain.get_output(output1, self.weights[1])
        output2 = Brain.get_output(output2, self.weights[2])
        output = Brain.get_output(output2, self.weights[3])
        if output[0] > 0.2 and 4 in available_commands: return 4, 0  # сбросить
        elif output[0] > 0.4 and 3 in available_commands: return 3, 0  # ва-банк
        elif output[0] > 0.6 and 2 in available_commands: return 2, 0  # пропустить
        elif output[0] > 0.8 and 1 in available_commands: return 1, 0  # уравнять
        elif output[0] > 1 and 0 in available_commands: return 0, output[1]  # поднять, output[1] - процент от допустимой ставки




