from random import randint
from tkinter import *
from functools import partial
import keyboard
import time

class Main():
    def __init__(self, xs, ys, bomb_count):
        # Создаём пустую карту
        self.map = self.createEmptyMap(xs, ys, 0)
        # Добавляем на карту бомбы
        coef = round(xs * ys / bomb_count)
        self.map = self.generateBombs(self.map, coef)
        # Добавляем на карту цифры
        self.map = self.generateNumbers(self.map)
        # Создаём пустую карту клеток которые 
        # пользователь проверил
        self.show = self.createEmptyMap(xs, ys, 0)
        # Отображаем карту
        self.time = time.time()
        self.timer_column = round(xs/2)
        self.play = True
        
        self.window = Tk()  
        self.window.title("Sapper") 
        self.window.geometry(f'{xs*31}x{ys*36+25}') 
        
        self.timer = Label(self.window, text='0:0')
        self.timer.grid(column=0, row=0)
        self.showMap(self.map)     
        
        
        self.updateTime()
        self.window.mainloop()
        
        
    # Создаём 2д массив заполненый placerом
    # с размером xs(ширина) и ys(длина) 
    def createEmptyMap(self, xs, ys, placer):
        return [[placer for i in range(xs)] for i in range(ys)]
        
    # Генерируем бомбы на карте
    def generateBombs(self, map, oneTo):
        for y in range(len(map)):
            for x in range(len(map[0])):
                # Если randint возращает 0 ставим в ячейку 10(мину)
                if randint(0, oneTo) == 0:
                    map[y][x] = 10
                # Иначе оставляем её пустой
                else:
                    map[y][x] = 0
        return map
    
    def generateNumbers(self, map):
        for x in range(len(map)):
            for y in range(len(map[0])): 
                # Если ячейка пустая
                if not map[x][y] == 10:
                    # Количество соседних бомб
                    s = 0
                    # Если есть бомба в верхней клетке +1
                    # try нужен чтобы избежать проблем с концом массива
                    try:
                        if map[x][y+1] == 10:
                            s += 1
                    except:
                        pass
                    
                    # Если есть бомба в нижней клетке +1
                    if map[x][y-1] == 10 and y > 0:
                        s += 1  
                        
                    # Если есть бомба левой верхней клетке +1
                    try:
                        if map[x-1][y+1] == 10 and x > 0:
                            s += 1
                    except:
                        pass
                    
                    # Если есть бомба в левой нижней клетке +1
                    if map[x-1][y-1] == 10 and y > 0 and x > 0:
                        s += 1  
                        
                    # Если есть бомба в правой верхней клетке +1
                    try:
                        if map[x+1][y+1] == 10:
                            s += 1
                    except:
                        pass
                    
                    # Если есть бомба в правой нижней клетке +1
                    try:
                        if map[x+1][y-1] == 10 and y > 0:
                            s += 1
                    except:
                        pass
                    
                    # Если есть бомба в левой клетке +1
                    if map[x-1][y] == 10 and x > 0:
                        s += 1
                    
                    # Если есть бомба в правой клетке +1
                    try:
                        if map[x+1][y] == 10 and x > 0:
                            s += 1
                    except:
                        pass 
                    
                    # Устанавливаем в клетку количество соседних с ней бомб
                    map[x][y] = s
        return map
    
    def showMap(self, map):
        # Массив(дисплей) того что нужно вывести на экран
        ftp = self.createEmptyMap(len(map[0]), len(map), '   ')
        
        
        for y, row in enumerate(map):
            # Выводим Y координату
            for x, item in enumerate(row):    
                # Если в клетке мина и её надо отобразить 
                # отображаем красную букву B
                if item == 10 and self.show[y][x] == 1:
                    ftp[y][x] = f'B'
                # Иначе если в клетке стоит флажок отображаем
                # красную букву F
                elif item > 10:
                    ftp[y][x] = f'F'
                # Иначе если в клетке любая другая цифра и её надо отобразить
                # то отображаем 0 белым, а любую другую цифры жёлтой
                elif self.show[y][x] == 1:
                    if not item == 0:
                        ftp[y][x] = f'{item}'
                    else:
                        ftp[y][x] = f'{item}'
                # Иначе если клетка не открыта отображаем белый ?
                else:
                    ftp[y][x] = f'?'
        # Выводим дисплей на экран
        self.showArray(ftp)
            
    def showArray(self, array):
        self.cleanWindow()
        
        self.timer = Label(self.window, text='0:0')
        self.timer.grid(column=self.timer_column, row=0)
        
        for y, row in enumerate(array):
            for x, item in enumerate(row):
                if item == '?':
                    Button(self.window, text=item, command=partial(self.click, x=x, y=y), height=2, width=3, fg='#808080').grid(column=x, row=y+1)
                elif item == '0':
                    Button(self.window, text=item, command=partial(self.click, x=x, y=y), height=2, width=3, fg='#808080').grid(column=x, row=y+1) 
                elif item == '1':
                    Button(self.window, text=item, command=partial(self.click, x=x, y=y), height=2, width=3, fg='#0000FF').grid(column=x, row=y+1) 
                elif item == '2':
                    Button(self.window, text=item, command=partial(self.click, x=x, y=y), height=2, width=3, fg='#00ff00').grid(column=x, row=y+1)
                elif item == '3':
                    Button(self.window, text=item, command=partial(self.click, x=x, y=y), height=2, width=3, fg='#FF0000').grid(column=x, row=y+1)
                else:
                    Button(self.window, text=item, command=partial(self.click, x=x, y=y), height=2, width=3, fg='#00007F').grid(column=x, row=y+1)
                
            
    def openZeros(self, map, checked, show, x, y):
        try:
            show[y][x+1] = 1
            if map[y][x+1] == 0 and not [x+1, y] in checked:
                checked.append([x+1, y])
                show = self.openZeros(map, checked, show, x+1, y)
        except:
            pass
        if x > 0:
            show[y][x-1] = 1
        if map[y][x-1] == 0 and not [x-1, y] in checked and x > 0:
            checked.append([x-1, y])
            show = self.openZeros(map, checked, show, x-1, y)
        try:
            show[y+1][x] = 1
            if map[y+1][x] == 0 and not [x, y+1] in checked:
                checked.append([x, y+1])
                show = self.openZeros(map, checked, show, x, y+1)
        except:
            pass
        if y > 0:
            show[y-1][x] = 1
        if map[y-1][x] == 0  and not [x, y-1] in checked and y > 0:
            checked.append([x, y-1])      
            show = self.openZeros(map, checked, show, x, y-1)
        return show
    
    def isWin(self, map):
        for y, row in enumerate(self.show):
            for x, item in enumerate(row):
                if item == 0 and not map[y][x] == 20:
                    return False
        for row in map:
            for item in row:
                # Если в клетке бомба возвращаем False
                if item == 10:
                    return False
                # Если в клетке флажок не на бомбе возвращаем False
                if item > 10 and not item == 20:
                    return False
        return True
            
    
    def click(self, x, y):
        if keyboard.is_pressed('f'):
            self.clickRight(x, y)
        else:
            self.clickLeft(x, y)
            
    def updateTime(self):       
        currentTime = time.time() - self.time
        self.timer['text'] = f'{round(currentTime)//60}:{round(currentTime)%60}'
        if self.play == True:
            self.last_time = time.time() - self.time
            self.window.after(3, self.updateTime)
            
        
            
    def cleanWindow(self):
        for widget in self.window.winfo_children():
            widget.destroy()
    
    def clickLeft(self, x, y):
        self.show[y][x] = 1
        if self.map[y][x] == 0:
            self.show = self.openZeros(self.map, [[x, y]], self.show, x, y)
        if self.map[y][x] == 10: 
            self.cleanWindow()
            Label(text='Game over!').grid(column=0, row=0)
            Button(text='New game', command=self.new_game).grid(column=0, row=1)
        else:
            self.showMap(self.map)
        if self.isWin(self.map) == True:
            self.play = False
            self.cleanWindow()
            Label(text='Win!').grid(column=0, row=0)
            Label(text=f'{round(self.last_time//60)}:{round(self.last_time%60)}').grid(column=0, row=1)
            Button(text='New game', command=self.new_game).grid(column=0, row=2)
            
    def clickRight(self, x, y):
        if self.map[y][x] < 11:
            if self.map[y][x] == 10:
                self.map[y][x] = 20
            else:
                self.map[y][x] = self.map[y][x]+11
            self.showMap(self.map)
        else:
            if self.map[y][x] == 20:
                self.map[y][x] = 10
            else:
                self.map[y][x] = self.map[y][x]-11
            self.showMap(self.map)
        if self.isWin(self.map) == True:
            self.play = False
            self.cleanWindow()
            Label(text='Win!').grid(column=0, row=0)
            Label(text=f'{round(self.last_time//60)}:{round(self.last_time%60)}').grid(column=0, row=1)
            Button(text='New game', command=self.new_game).grid(column=0, row=2)
            
    def closeWindow(self):
        self.window.destroy()
        
    def new_game(self):
        self.closeWindow()
        new_game()

def new_game():
    Tk().destroy()
    
    window = Tk()  
    window.title("Sapper") 
    window.geometry('300x108') 

    height = Entry(window)
    height.grid(column=1, row=0)
    width = Entry(window)
    width.grid(column=1, row=1)
    bombs = Entry(window)
    bombs.grid(column=1, row=2)

    text = Label(window, text="Height").grid(column=0, row=0)
    text2 = Label(window, text="Width").grid(column=0, row=1)
    text3 = Label(window, text="Bombs count").grid(column=0, row=2)
    
    Button(window, text='Play', command=partial(start, height, width, bombs, window)).grid(column=1, row=3)
    window.mainloop()

def start(height, width, bombs, window):
    height_r = int(height.get())
    width_r = int(width.get())
    bombs_r = int(bombs.get())
    window.destroy()
    main = Main(height_r, width_r, bombs_r)
    while True:
        pass


new_game()