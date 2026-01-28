from collections import OrderedDict
from math import floor
import random
import schedule
import time
import tkinter as tk
import keyboard

CELL_SIZE = 50,50

class Snake:
    def __init__(self,root):
        self.headId = 1
        self.segments = {
            1:{
                'direction':(1,0),
                'x':2,
                'y':0
            },
            2:{
                'direction':(1,0),
                'x':1,
                'y':0
            },
            3:{
                'direction':(1,0),
                'x':0,
                'y':0
            },
        }
        self.root = root

    def getLocation(self,id=None):
        return self.segments
    
    def moveSnake(self):
        tail =  self.segments.get(sorted(self.segments.keys())[-1]).copy()
        for idx,item in OrderedDict(reversed(list(self.segments.items()))).items():
            originalX = item.get('x')
            originalY = item.get('y')
            direction = item.get('direction')
            self.segments.get(idx).update({'x':originalX + direction[0],'y':originalY + direction[1]})
            try:
                prevDirection = self.segments.get(idx-1).get('direction')
            except:
                prevDirection = self.segments.get(idx).get('direction')

            self.segments.get(idx).update({'direction':prevDirection})
        return tail
    def add_segment(self):
        segments_list = list(self.segments.items())
        last_id = segments_list[-1][0]
        last_x = segments_list[-1][1].get('x')
        last_y = segments_list[-1][1].get('y')
        last_direction = segments_list[-1][1].get('direction')
        segments_list.append((last_id+1, {'direction': last_direction, 'x': last_x - last_direction[0], 'y': last_y - last_direction[1]}))
        self.segments = dict(segments_list)
        


def createWindow(cell_size):
    root = tk.Tk()

    root.title("Snake")
    root.configure(background="lightgray")
    root.resizable(False, False)


    for i in range(15):
        for j in range(20):
            e = tk.Frame(root, width=cell_size[0],height=cell_size[1])
            e['background'] = 'lightgray'
            e.grid(row=i,column=j)
    root.grid_slaves()
    return root

def showGridlines(root):
    cells = root.grid_slaves()
    for cell in cells:
        cell['borderwidth']=1,
        cell['relief']='sunken'

def getGridCenter(root):
    grid = root.grid_size()

    y_center = floor(grid[0]/2)
    x_center = floor(grid[1]/2)

    return x_center,y_center

def getCellFromCords(root,cords):
    cell = root.grid_slaves(cords[0],cords[1])[0]

    return cell

def showSnake(root,snake:Snake):
    seg = snake.segments.get(1)
    cell = getCellFromCords(root,(seg['x'],seg['y']))
    cell['background'] = 'green'

def turnOffCell(root,seg):
    cell = getCellFromCords(root,(seg['x'],seg['y']))
    cell['background'] = 'lightgray'

def checkCollision(snake:Snake,root:tk.Tk):
    size = root.grid_size()
    head = snake.segments.get(1)
    if head.get('y') + head.get('direction')[1] < 0 or head.get('y') + head.get('direction')[1] >= size[0]:
        raise Exception("Sorry, out of bounds")
    if head.get('x') + head.get('direction')[0] < 0 or head.get('x') + head.get('direction')[0] >= size[1]:
        raise Exception("Sorry, out of bounds")

    for segment in snake.segments.values():
        if head.get('y') + head.get('direction')[1] == segment.get('y') and head.get('x') + head.get('direction')[0] == segment.get('x'):
            raise Exception("Sorry, no hitting yourself")

def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval,1, periodic,
                    (scheduler, interval, action, actionargs))
    action(*actionargs)

def generateRandomCords(size):

    x = random.randint(0, size[1]-1)
    y = random.randint(0, size[0]-1)
    return x,y 
def spawnFood(snake:Snake,root:tk.Tk):
    size = root.grid_size()

    while True:
        cords = generateRandomCords(size)

        for seg in snake.segments.values():
            if seg.get('x') == cords[0] and seg.get('y') == cords[1]:
                continue
        break
    print(cords)
    cell = getCellFromCords(root,cords)
    cell['background'] = 'red'
    return cords
def checkFood(snake:Snake,appleCords):
    head = snake.segments.get(1)
    if head['x'] == appleCords[0] and head['y'] == appleCords[1]:
        return True
    return False
def updateSnake(snake:Snake,root):
    global noFood
    global foodLoc
    if noFood:
        foodLoc = spawnFood(snake,root)
        noFood = False
    checkCollision(snake,root)
    noFood = checkFood(snake,foodLoc)
    tail = snake.moveSnake()
    if noFood:
        snake.add_segment()
    showSnake(root,snake)
    turnOffCell(root,tail)
    root.update()

def changeDirection(x,y,snake:Snake):
    snake.segments.get(1).update({'direction':(x,y)})


if __name__=='__main__':

    root = createWindow(CELL_SIZE)

    showGridlines(root)
    snake = Snake(root)
    keyboard.add_hotkey('down', changeDirection,(1,0,snake))
    keyboard.add_hotkey('up', changeDirection,(-1,0,snake))
    keyboard.add_hotkey('left', changeDirection,(0,-1,snake))
    keyboard.add_hotkey('right', changeDirection,(0,1,snake))
    showSnake(root,snake)
    root.update()
    global noFood
    noFood = True
    schedule.every(0.15).seconds.do(updateSnake,snake,root)

    keyboard.read_event()


    while True:
        schedule.run_pending()
