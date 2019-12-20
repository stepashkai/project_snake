import random
from tkinter import *
from PIL import Image, ImageTk
#Задает ширину игровой области
WIDTH = 1000
#Задает высоту игровой области
HEIGHT = 700
#Задает рамзеры одной ячейки тела змейки и площади одного яблока(они задаются квадратами)
BODYSIZE = 50
#Задает начальную скорость передвижения змейки(задается в миллисикунадх между каждым перемещением змейки)
STARTDELAY = 300
#Задает максимальную скорость передвижения змейки
MINDELAY = 100
#Задает увеличение скорости змейки после поедания одного яблока
STEPDELAY = 20
#Задает начальную длину змейки
LENGTH = 6

countBodyW = WIDTH / BODYSIZE
countBodyH = HEIGHT / BODYSIZE
'''class Snake: содержит в себе основные функции для игры Snake.
Является дочерним от класса Canvas, с помощью которого создаются объекты-холсты,
на которых можно "рисовать", размещая различные фигуры и объекты.'''
class Snake(Canvas):
    #Задаем начальные координаты
    x = False
    y = False
    #Задаем изображения головы змейки
    headImage = False
    #Задаем переменные для изображений змейки
    head = False
    body = False
    apple = False
    #Задаем начальное
    delay = 0
    #Задаем направление головы змейки (второе может изменяться)
    direction = "Right"
    directiontemp = "Right"
    #Задаем переменную, в которой содержится проиграли ли мы или нет
    loss = False
    #Задаем переменную для кнопок главного меню
    button = False
    '''def __init__(self): является функцией-конструктором для класса змейки, подстраиваясь под
    заданные пользователем рамзеры змейки,под выбранный фон.'''
    def __init__(self):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT, background="green", highlightthickness=0)
        self.focus_get()
        self.bind_all("<Key>", self.onKeyPressed)
        self.loadResources()
        self.MainScreen()
        self.pack()
    ''' def loadResources(self): загружает изображения головы змейки,
    ее туловища и яблока из папки images для дальнейшего вывода их в игровую область.'''
    def loadResources(self):
        self.headImage = Image.open("images/head.png")

        self.head = ImageTk.PhotoImage(self.headImage.resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))
        self.body = ImageTk.PhotoImage(Image.open("images/body.png").resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))
        self.apple = ImageTk.PhotoImage(Image.open("images/apple.png").resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))
    '''def beginplay(self): функция, которая задает начало игры,
    удаляя кнопки главного меню. Также задает начальные координаты змейки,
    начальное положение головы, задает начальное время задержки между 
    каждым передвижением змейки на одну ячейку. Так же при генерации змейки сразу
    проиграть невозможно, что обеспечивает переменная loss = False. В случае последующей
    попытки очищает экран и начинает игру сначала.'''
    def beginplay(self):
        destroy_object = [self.button, self.button2]
        for object_name in destroy_object:
            object_name.destroy()
        self.delay = STARTDELAY
        self.direction = "Right"
        self.directiontemp = "Right"
        self.loss = False

        self.x = [0] * int(countBodyW)
        self.y = [0] * int(countBodyH)

        self.delete(ALL)
        self.spawnActors()
        self.after(self.delay, self.timer)
    '''def MainScreen(self): с помощью этой функции генерируется главное меню игры, создавая 
    две кнопки: 'Начать игру','Выйти из игры'.'''
    def MainScreen(self):
        self.button = Button(root, text='Начать игру', command=self.beginplay)
        self.button.pack()
        self.button2 = Button(root, text='Выйти из игры', command=self.quit)
        self.button2.pack()
    '''def SpawnActors(self): генерирует яблоко в игровой области, а также с помощью цикла
    обновляет изображение(длину) змейки.'''
    def spawnActors(self):

        self.spawnApple()

        self.x[0] = int(countBodyW / 2) * BODYSIZE
        self.y[0] = int(countBodyH / 2) * BODYSIZE
        for i in range(1, LENGTH):
            self.x[i] = self.x[0] - BODYSIZE * i
            self.y[i] = self.y[0]
        self.create_image(self.x[0], self.y[0], image=self.head, anchor="nw", tag="head")
        for i in range(LENGTH - 1, 0, -1):
            self.create_image(self.x[i], self.y[i], image=self.body, anchor="nw", tag="body")
    '''def spawnApple(self): функция генерирует яблоко в игровой области в произвольном месте'''
    def spawnApple(self):
        apple = self.find_withtag("apple")
        if apple:
            self.delete(apple[0])
        rx = random.randint(0, countBodyW - 1)
        ry = random.randint(0, countBodyH - 1)
        self.create_image(rx * BODYSIZE, ry * BODYSIZE, anchor="nw", image=self.apple, tag="apple")
    '''def checkApple(self): проверяет наличие коллизии яблока со змейкой.'''
    def checkApple(self):
        apple = self.find_withtag("apple")[0]
        head = self.find_withtag("head")
        body = self.find_withtag("body")[-1]
        x1, y1, x2, y2 = self.bbox(head)
        overlaps = self.find_overlapping(x1, y1, x2, y2)
        for actor in overlaps:
            if actor == apple:
                tempx, tempy = self.coords(body)
                self.spawnApple()
                self.create_image(tempx, tempy, image=self.body, anchor="nw", tag="body")
                if self.delay > MINDELAY:
                    self.delay -= STEPDELAY
    '''def checkCollisions(self): проверяет пересечение змейки со свои хвостом, а также с краями
    игровой области. Если голова пересекает один из этих объектов, то переменная loss становится равной
    True, что приводит к завершению игры.'''
    def checkCollisions(self):
        head = self.find_withtag("head")
        body = self.find_withtag("body")
        x1, y1, x2, y2 = self.bbox(head)
        overlaps = self.find_overlapping(x1, y1, x2, y2)
        for b in body:
            for actor in overlaps:
                if actor == b:
                    self.loss = True

        if x1 < 0:
            self.loss = True
        if x2 > WIDTH:
            self.loss = True
        if y1 < 0:
            self.loss = True
        if y2 > HEIGHT:
            self.loss = True
    '''def onKeyPressed(self): проверяет нажатие клавиш и в соответствии с нажатой клавишей изменяет
    направление движения змейки (причем изменять направление движения в сторону, противоположную
    текущему движению змейки нельзя, так как это приведет к завершению игры). Также, если после
    поражения пользователь решит начать игру заново, то ему нужно будет нажать на клавишу 'space', что
    приведет к повторной попытке.'''
    def onKeyPressed(self, event):
        key = event.keysym
        if key == "Left" and self.direction != "Right":
            self.directiontemp = key
        elif key == "Right" and self.direction != "Left":
            self.directiontemp = key
        elif key == "Up" and self.direction != "Down":
            self.directiontemp = key
        elif key == "Down" and self.direction != "Up":
            self.directiontemp = key
        elif key == "space" and self.loss:
            self.beginplay()
    '''def updateDirection(self): с помощью этой функции голова змейки всегда остается в "правильном" положении (то есть,
    например, если змейка движется вправо, а пользователь решит изменить направление движения
    змейки вверх, то она будет "смотреть" вверх, а не вправо, если бы не отсутствие данной функции)'''
    def updateDirection(self):
        self.direction = self.directiontemp
        head = self.find_withtag("head")
        headx, heady = self.coords(head)
        self.delete(head)
        if self.direction == "Left":
            self.head = ImageTk.PhotoImage(self.headImage.transpose(Image.FLIP_LEFT_RIGHT).resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))
        else:
            rotates = {"Right": 0, "Up": 90, "Down": - 90}
            self.head = ImageTk.PhotoImage(self.headImage.rotate(rotates[self.direction]).resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))

        self.create_image(headx, heady, image=self.head, anchor="nw", tag="head")
    '''def timer(self): "собирательная" функция, обеспечивающая игру всей змейки. Если игра идет, то
    запускаются все функции, кроме функции gameOver(self), которая приостанавливает цикл перемещения
    змейки.'''
    def timer(self):
        self.checkCollisions()
        if not self.loss:
            self.checkApple()
            self.updateDirection()
            self.moveSnake()
            self.after(self.delay, self.timer)
        else:
            self.gameOver()
    '''def moveSnake(self): с помощью этой функции обеспечивается перемещение изображения змейки.
    Принцип состоит в том, чтобы каждый раз удалять старое изображение и генерировать новое, но смещенное
    в соответствии с текущим направлением змейки.'''
    def moveSnake(self):
        head = self.find_withtag("head")
        body = self.find_withtag("body")
        items = body + head
        for i in range(len(items) - 1):
            currentxy = self.coords(items[i])
            nextxy = self.coords(items[i + 1])
            self.move(items[i], nextxy[0] - currentxy[0], nextxy[1] - currentxy[1])
        if self.direction == "Left":
            self.move(head, -BODYSIZE, 0)
        elif self.direction == "Right":
            self.move(head, BODYSIZE, 0)
        elif self.direction == "Up":
            self.move(head, 0, -BODYSIZE)
        elif self.direction == "Down":
            self.move(head, 0, BODYSIZE)
    '''def gameOver(self): в случае поражения данная функция удаляет все изображения змейки и яблока,
    а выводит уведомление о проигрыше, выводит рекорд, а также предложение начать игру заново.'''
    def gameOver(self):
        body = self.find_withtag("body")
        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 - 60, text="Вы проиграли!", fill="white", font="Tahoma 40", tag="text")
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2, text="Длина змейки: " + str(len(body) + 1), fill="white", font="Tahoma 40", tag="text")
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 + 60, text="Нажмите пробел для новой игры", fill="white", font="Tahoma 40", tag="text")


root = Tk()
root.title("Змейка")

root.board = Snake()

root.resizable(False, False)

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

x = int(ws / 2 - WIDTH / 2)
y = int(hs / 2 - HEIGHT / 2)

root.geometry("+{0}+{1}".format(x, y))

root.mainloop()

