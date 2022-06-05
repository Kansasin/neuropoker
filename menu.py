from os import system

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
        if cls: system('cls')
        print(self.get_label() + '\n')
        if len(self.get_options()) == 0: return self.text_input.print_input()
        options_str = ''
        for i in range(len(self.get_options())):
            options_str += f'{i + 1}. {self.get_options()[i].get_text()}\n'
        print('\n' + options_str + '\n')
        answer = self.text_input.print_input().split(' ')
        if not (answer[0].isdigit() and 1 <= int(answer[0]) <= len(self.get_options())): return self.print_menu()
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
