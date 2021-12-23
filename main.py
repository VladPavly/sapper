from random import randint
from colorama import Fore, Back, Style

class Main():
    def __init__(self, xs, ys):
        self.map = self.createEmptyMap(xs, ys, 0)
        self.map = self.generateBombs(self.map, 40)
        self.map = self.generateNumbers(self.map)
        self.show = self.createEmptyMap(xs, ys, 0)
        self.showMap(self.map)
        
        
    def createEmptyMap(self, xs, ys, placer):
        return [[placer for i in range(xs)] for i in range(ys)]
        
    def generateBombs(self, map, oneTo):
        for y in range(len(map)):
            for x in range(len(map[0])):
                if randint(0, oneTo) == 0:
                    map[y][x] = 10
                else:
                    map[y][x] = 0
        return map
    
    def generateNumbers(self, map):
        for x in range(len(map)):
            for y in range(len(map[0])): 
                if not map[x][y] == 10:
                    s = 0
                    try:
                        if map[x][y+1] == 10:
                            s += 1
                    except:
                        pass
                    if map[x][y-1] == 10 and y > 0:
                        s += 1  
                    try:
                        if map[x-1][y+1] == 10 and x > 0:
                            s += 1
                    except:
                        pass
                    if map[x-1][y-1] == 10 and y > 0 and x > 0:
                        s += 1  
                    try:
                        if map[x+1][y+1] == 10:
                            s += 1
                    except:
                        pass
                    try:
                        if map[x+1][y-1] == 10 and y > 0:
                            s += 1
                    except:
                        pass  
                    if map[x-1][y] == 10 and x > 0:
                        s += 1
                    try:
                        if map[x+1][y] == 10 and x > 0:
                            s += 1
                    except:
                        pass 
                    map[x][y] = s
        return map
    
    def showMap(self, map):
        ftp = self.createEmptyMap(len(map[0])+1, len(map)+1, '   ')
        for x in range(len(map[0])):
            ftp[0][x+1] = f'{x} '
        #print    
        for y, row in enumerate(map):
            ftp[y+1][0] = f'{y} '
            for x, item in enumerate(row):
                if item == 10 and self.show[y][x] == 1:
                    ftp[y+1][x+1] = f'{Fore.RED}B  {Fore.RESET}'
                elif item > 10:
                    ftp[y+1][x+1] = f'{Fore.RED}F  {Fore.RESET}'
                elif self.show[y][x] == 1:
                    if not item == 0:
                        ftp[y+1][x+1] = f'{Fore.YELLOW}{item}  {Fore.RESET}'
                    else:
                        ftp[y+1][x+1] = f'{Fore.WHITE}{item}  {Fore.RESET}'
                else:
                    ftp[y+1][x+1] = f'{Fore.WHITE}?  {Fore.RESET}'
            #print
        self.showArray(ftp)
            
    def showArray(self, array):
        for row in array:
            tp = ''
            for item in row:
                if len(item) == 2:
                    tp += f'{item} '
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