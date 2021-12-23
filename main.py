from random import randint
from colorama import Fore, Back, Style

class Main():
    def __init__(self, xs, ys):
        # Создаём пустую карту
        self.map = self.createEmptyMap(xs, ys, 0)
        # Добавляем на карту бомбы
        self.map = self.generateBombs(self.map, 40)
        # Добавляем на карту цифры
        self.map = self.generateNumbers(self.map)
        # Создаём пустую карту клеток которые 
        # пользователь проверил
        self.show = self.createEmptyMap(xs, ys, 0)
        # Отображаем карту
        self.showMap(self.map)
        
        
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
        ftp = self.createEmptyMap(len(map[0])+1, len(map)+1, '   ')
        
        # Выводим X координаты
        for x in range(len(map[0])):
            ftp[0][x+1] = f'{x} '
        
        
        for y, row in enumerate(map):
            # Выводим Y координату
            ftp[y+1][0] = f'{y} '
            for x, item in enumerate(row):    
                # Если в клетке мина и её надо отобразить 
                # отображаем красную букву B
                if item == 10 and self.show[y][x] == 1:
                    ftp[y+1][x+1] = f'{Fore.RED}B  {Fore.RESET}'
                # Иначе если в клетке стоит флажок отображаем
                # красную букву F
                elif item > 10:
                    ftp[y+1][x+1] = f'{Fore.RED}F  {Fore.RESET}'
                # Иначе если в клетке любая другая цифра и её надо отобразить
                # то отображаем 0 белым, а любую другую цифры жёлтой
                elif self.show[y][x] == 1:
                    if not item == 0:
                        ftp[y+1][x+1] = f'{Fore.YELLOW}{item}  {Fore.RESET}'
                    else:
                        ftp[y+1][x+1] = f'{Fore.WHITE}{item}  {Fore.RESET}'
                # Иначе если клетка не открыта отображаем белый ?
                else:
                    ftp[y+1][x+1] = f'{Fore.WHITE}?  {Fore.RESET}'
        # Выводим дисплей на экран
        self.showArray(ftp)
            
    def showArray(self, array):
        for row in array:
            # Строка которую надо вывести
            tp = ''
            for item in row:
                # Если строка имеет длину 2 добавить к ней пробел
                # и отобразить
                if len(item) == 2:
                    tp += f'{item} '
                # В остальных случаях отобразить строку
                else:
                    tp += item
            print(tp)
            
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
        for row in map:
            for item in row:
                if item == 10:
                    return False
                if item > 10 and not item == 20:
                    return False
        return True
            


height = int(input('Enter a height: '))       
width = int(input('Enter a width: '))     
        
main = Main(height, width)
while True:
    text_input = input('Enter the X, Y: ')
    x = int(text_input.split(', ')[0])
    y = int(text_input.split(', ')[1])
    text_input = input('Check, flag or unflag: ')
    if text_input == 'check':
        main.show[y][x] = 1
        if main.map[y][x] == 0:
            main.show = main.openZeros(main.map, [[x, y]], main.show, x, y)
        main.showMap(main.map)
        if main.map[y][x] == 10:
            print('Game over!')
            break
    elif text_input == 'flag':
        if main.map[y][x] == 10:
            main.map[y][x] = 20
        else:
            main.map[y][x] = main.map[y][x]+11
        main.showMap(main.map)
    elif text_input == 'unflag':
        if main.map[y][x] == 20:
            main.map[y][x] = 10
        else:
            main.map[y][x] = main.map[y][x]-11
        main.showMap(main.map)
    if main.isWin(main.map):
        print('Win!')
        break
