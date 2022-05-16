import turtle

class LSystem2D:
    def __init__(self, t, axiom, width, length, angle):
        self.axiom = axiom      # инициатор
        self.state = axiom      # строка с набором команд для фрактала (вначале это инициатор)
        self.width = width      # толщина линии рисования
        self.length = length    # длина одного линейного сегмента кривой
        self.angle = angle      # фиксированный угол поворота
        self.t = t              # сама черепашка
        self.rules = {}  # словарь для хранения правил формирования кривых
        self.t.pensize(self.width)

    def add_rules(self, *rules):
        for key, value in rules:
            self.rules[key] = value

    def generate_path(self, n_iter):
        for n in range(n_iter):
            for key, value in self.rules.items():
                self.state = self.state.replace(key, value.lower())

            self.state = self.state.upper()

    def draw_turtle(self, start_pos, start_angle):
         # ***************
        turtle.tracer(1, 0)         # форсажный режим для черепашки
        self.t.up()                 # черепашка поднимается
        self.t.setpos(start_pos)    # начальная стартовая позиция
        self.t.seth(start_angle)    # начальный угол поворота
        self.t.down()               # черепашка опускается
        # ***************
        for move in self.state:
            if move == 'F':                 #Проход с отрисовкой
                self.t.forward(self.length)
            elif move == 'S':               #Проход без отрисовки (f в лекции)
                self.t.up()
                self.t.forward(self.length)
                self.t.down()
            elif move == '+':               #Повороты
                self.t.left(self.angle)
            elif move == '-':
                self.t.right(self.angle)

        turtle.done()        # чтобы окно не закрывалось после отрисовки



width = 1200
height = 600
screen = turtle.Screen()
screen.setup(width, height, 0, 0)

t = turtle.Turtle()
t.ht()          # скрываем черепашку

pen_width = 2         # толщина линии рисования (в пикселах)
f_len = 4             # длина одного сегмента прямой (в пикселах)
angle = 60            # фиксированный угол поворота (в градусах) для Снежинки
#angle = 90           # Для ковра или дракона
#axiom = "FX"         # Дракон хартвея 1
#axiom = "F-F-F-F"    # Ковер серпинского 1
axiom = "F--F--F"     # Сжнежинка коха 1

l_sys = LSystem2D(t, axiom, pen_width, f_len, angle)
#l_sys.add_rules(("FX","FX+FY+"),("FY","-FX-FY")) #Дракон хартвея 2
#l_sys.add_rules(("F","FF-F-F-F-FF")) # Ковер серпинского 2
l_sys.add_rules(("F", "F+F--F+F")) #Снежинка коха 2
l_sys.generate_path(1) #кол-во итераций. Для ковра оптимально 4, для снежинки 5, для дракона 12-13
print(l_sys.state)     #Вывод конечной инструкции 
l_sys.draw_turtle( (0, 0), 0)
