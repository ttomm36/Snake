from collections import OrderedDict
from math import floor
import schedule
import time
import tkinter as tk

CELL_SIZE = 50,50

class Snake:
    def __init__(self,root,location):
        self.headId = 1
        self.segments = {
            1:{
                'direction':(0,1),
                'x':location[0],
                'y':location[1]
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
        self.location = location
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

def createWindow(cell_size):
    root = tk.Tk()

    root.title("Snake")
    root.configure(background="lightgray")
    root.resizable(False, False)


    for i in range(15):
        for j in range(15):
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
    for seg in snake.segments.values():
        cell = getCellFromCords(root,(seg['x'],seg['y']))
        cell['background'] = 'red'

def turnOffCell(root,seg):
    cell = getCellFromCords(root,(seg['x'],seg['y']))
    cell['background'] = 'lightgray'

def checkCollision():
    pass

def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval,1, periodic,
                    (scheduler, interval, action, actionargs))
    action(*actionargs)

def update_snake(snake,root):
    tail = snake.moveSnake()
    showSnake(root,snake)
    turnOffCell(root,tail)
    root.update()

if __name__=='__main__':

    root = createWindow(CELL_SIZE)

    showGridlines(root)
    # getGridCenter(root)
    snake = Snake(root,(2,0))
    showSnake(root,snake)
    root.update()

    schedule.every(0.5).seconds.do(update_snake,snake,root)

    while True:
        schedule.run_pending()

    root.mainloop()

