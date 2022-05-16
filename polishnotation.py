import math


def infix_to_postfix_5(infix_notation, delimetr=""):
    """
    convertion for multiple digits
    with parentheses, unary minus and cos
    """
    stack = []
    RPM = []

    strength = {
        "+": 1,
        "-": 1,
        "*": 2,
        "^": 3,
        "/": 2,
        "cos": 2,
        "sin": 2,
        "sqrt": 2,
        "(": -1
    }

    i = 0
    while i < len(infix_notation):
        char: str = infix_notation[i]
        if char.isdigit():
            num = f"{char}"
            if i < len(infix_notation) - 1:
                while i < len(infix_notation) - 1:
                    if not (infix_notation[i + 1].isdigit() or infix_notation[i + 1] == "."):
                        break

                    num += infix_notation[i + 1]
                    i += 1

            i += 1
            num += delimetr
            RPM.append(num)
            if i > 1:
                if infix_notation[i - 1] == "-" and infix_notation[i - 2] == "(":
                    RPM.append("-")

        elif char in "-+*/()^":
            if len(stack) > 0:
                if not char in "()":

                    last_char = stack[-1]
                    if not last_char in ["(", ")"]:
                        if strength[char] > strength[last_char]:
                            stack.append(char)
                            i += 1
                        else:
                            while (
                                len(stack) > 0 and strength[char] <= strength[stack[-1]]
                            ):
                                if stack[-1] == "(":
                                    break
                                last_char = stack.pop()
                                RPM.append(last_char)
                            stack.append(char)
                            i += 1
                    else:
                        if (
                            infix_notation[i - 1] == "("
                            and char == "-"
                        ):
                            RPM.append("0" + delimetr)
                            stack.append("-")
                        #     RPM.append("-")
                        else:
                            stack.append(char)
                        i += 1
                else:
                    if char == "(":
                        stack.append(char)
                        i += 1
                    elif char == ")":
                        last_char = stack.pop()
                        while len(stack) > 0 and last_char != "(":
                            RPM.append(last_char)
                            last_char = stack.pop()
                        i += 1
            else:
                if char == "-":
                    RPM.append("0" + delimetr)
                    stack.append("-")
                else:
                    stack.append(char)
                i += 1
        elif char.isalpha():
            if infix_notation[i:i+3] == 'cos':
                RPM.append("0")
                stack.append('cos')
                i += 3
            elif infix_notation[i:i+3] == 'sin':
                RPM.append("0")
                stack.append('sin')
                i += 3
            elif infix_notation[i:i+4] == 'sqrt':
                RPM.append("0")
                stack.append('sqrt')
                i += 4

    # simply getting operations from stack and passing them to RPM
    for char in stack[::-1]:
        RPM.append(char)
    return RPM

def postfix_calculation(RPM):
    def calculate_nums(num_1, num_2, sign):
        global result
        if sign == "+":
            result = num_1 + num_2
        elif sign == "-":
            result = num_1 - num_2
        elif sign == "/":
            result = num_1 / num_2
        elif sign == "*":
            result = num_1 * num_2
        elif sign == 'cos':
            result = math.cos(num_2)
        elif sign == 'sin':
            result = math.sin(num_2)
        elif sign == 'sqrt':
            result = math.sqrt(num_2)
        elif sign == '^':
            result = num_1 ** num_2

        return result

    numbers_stack = []

    i = 0
    while i < len(RPM):
        item = RPM[i]
        if item[0].isdigit():
            numbers_stack.append(float(item))
        else:
            num_1 = numbers_stack.pop()
            num_2 = numbers_stack.pop()
            sign = item
            result_operation = calculate_nums(num_2, num_1, sign)
            numbers_stack.append(result_operation)
        i += 1

    return numbers_stack[0]


# examples = [["5+(6.6+9-5.2)/(0.8+1*2)+7", "0;5;-+6.6;9;+5.2;0.8;1;2;*+/7;+"]]
# examples = [["-55+(-60.70-9)*(-7)-(120+3*4.56)/(-22)", "569-7*+"]]
# examples = [["-(-3.5+2*2.25)*7+1*cos(1+5*4)", "569-7*+"]]
examples = [
    # '1+2*(3+4/2-cos(1+2))*2+1',
    # "-sqrt(-3.5+2*2.25)*7^0.5+1*cos(1+5*4)*(sin(3+5*6)+2)*sqrt(123+4*5+12)^3",
   #"-sqrt(-3+2*2)*7+1*(1+5*4)*(3+5*6+2)*sqrt(1+4*5+1)",
    # "-2*(2+3*2)*2"
    # "((1*2)+3)",
     "2.5",
     "3+sqrt(5)*6/6+sqrt(7)"
]

# 05-+69+58;1;2;*+/7;++
for item in examples:
    RPM = infix_to_postfix_5(item, delimetr="")
    # if predict != item[1]:
    print("".join(RPM))

    result = postfix_calculation(RPM)
    eval_result = "exec('from math import *') or "+item
    eval_result = eval_result.replace("^", "**")
    print(result, eval(eval_result))
    # print(f"{item[1]}\n{predict}")

    # добавить корень, синусы, косинусы, степени

    # метод рекурсивного спуска, L1 грамматика, метод нисходящего спуска
