"""
(1) E => E + T
(2) E => T
(3) T => T ∗ F
(4) T => F
(5) F => (E)
(6) F => x
"""


class Grammar:
    def __init__(self):
        #Объявляем правила
        self.rules = {
            1: ["E", "E+T"],
            2: ["E", "T"],
            3: ["T", "T*F"],
            4: ["T", "F"],
            5: ["F", "(E)"],
            6: ["F", "x"]
        }

    def __getitem__(self, key):
        return self.rules[key]


class Goto:
    #Класс описывающий таблицу переходов
    def __init__(self):
        self.goto_column_pos = {
            "E": 0,
            "T": 1,
            "F": 2
        }

        self.goto_table = [
            [1, 2, 3],
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1],
            [8, 2, 3],
            [-1, -1, -1],
            [-1, 9, 3],
            [-1, -1, 10],
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1],
        ]

    def __getitem__(self, key):
        pos, char = key
        column_pos = self.goto_column_pos[char]
        return self.goto_table[pos][column_pos]


class Action:
    def __init__(self):
        self.action_table = [
            ["s5", "", "", "s4", "", ""],
            ["", "s6", "", "", "", "acc"],
            ["", "r2", "s7", "", "r2", "r2"],
            ["", "r4", "r4", "", "r4", "r4"],
            ["s5", "", "", "s4", "", ""],
            ["", "r6", "r6", "", "r6", "r6"],
            ["s5", "", "", "s4", "", ""],
            ["s5", "", "", "s4", "", ""],
            ["", "s6", "", "", "s11", ""],
            ["", "r1", "s7", "", "r1", "r1"],
            ["", "r3", "r3", "", "r3", "r3"],
            ["", "r5", "r5", "", "r5", "r5"]
        ]

        self.action_column_pos = {
            "x": 0,
            "+": 1,
            "*": 2,
            "(": 3,
            ")": 4,
            "$": 5
        }

    def __getitem__(self, key):
        char, pos = key
        column_pos = self.action_column_pos[char]
        return self.action_table[pos][column_pos]


class LR_Parser:
    def __init__(self, input_string):
        self.action = Action()
        self.goto = Goto()
        self.grammar = Grammar()

        self.input_string = f"{input_string}$"
        self.cur_pos = 0

    def parse(self):
        # стек где мы будем хранить символы после преобразований и новые символы строки
        char_stack = []
        # сначала мы находимся в нулевом состоянии
        state_stack = [0]
        # первый входной символ это первый символ строки
        input_char = self.input_string[self.cur_pos]
        # последнее состояние со стека состояний
        state = state_stack[-1]

        # принята наша строка или нет
        is_accepted = False
        production_num = 0
        # мы не можем заранее знать сколько шагов нам понадобится
        # так как условие остановки возникает в процессе обработки строки
        while True:
            # на каждой итерации мы берем последнее состояние со стека (не удаляя его)
            state = state_stack[-1]
            # по входному символу и текущему состоянию берем из таблицы следующее действие
            action_type = self.action[input_char, state]
            # переменная которая отображает количество пройденной строки
            input_string_print = self.input_string[self.cur_pos:]
            # стока для отображения текущего стека состояний
            state_stack_print = " ".join(map(str, state_stack))
            # переменная для отображения свертки\сдвига\принятия
            action_type_print = ""

            # если мы достигли конца обработки строки
            if action_type == "acc":
                action_type_print = "Accepted"
                char_stack_print = "".join(char_stack)
                is_accepted = True
                break

            # если тип действия это сдвиг
            if 's' in action_type:
                action_type_print = action_type
                # номер следующего состояния
                state = int(action_type[1:])
                state_stack.append(state)
                # перемещаем указатель в строке
                self.cur_pos += 1
                char_stack_print = "".join(char_stack)
                # добавляем с стек символов текущий входной символ
                char_stack.append(input_char)
                # определяем следующий входной символ
                input_char = self.input_string[self.cur_pos]

            # если тип действия это свертка
            elif 'r' in action_type:
                # определяес номер продукции, которую должны применить к строке
                production_num = int(action_type[1:])
                # берем саму продукцию
                rule = self.grammar[production_num]
                # узнаем длину продукции
                right_rule_len = len(rule[1])
                # превращаем содержимое стека символов в строку
                char_stack_print = "".join(char_stack)
                # удаляем последние символы со стека символов и состояний в количестве right_rule_len
                char_stack = char_stack[:-right_rule_len]
                state_stack = state_stack[:-right_rule_len]
                # добавляем левую часть продукции в стек символов
                char_stack.append(rule[0])

                # берем последнее состояние со стека состояний
                state = state_stack[-1]
                # по таблице goto определяем следующее состояние
                goto_state = self.goto[state, rule[0]]
                # добавляем это состояние в стек состояний
                state_stack.append(goto_state)
                # превращаем продукцию в печатную строку
                action_type_print = "->".join(rule)
            else:
                char_stack_print = "".join(char_stack)
                action_type_print = "Syntax Error"
                print(f"{state_stack_print:20}{char_stack_print:10}{input_string_print:25}{action_type_print}")
                break
            if not "s" in action_type:
                print(f"{char_stack_print}{input_string_print} => ({action_type_print})({production_num}) \n", end=" ")
        if is_accepted:
            print(f"{char_stack_print}{input_string_print} => ({action_type_print})({production_num}) \n", end=" ")


parser = LR_Parser("x+(x*x)")
parser.parse()