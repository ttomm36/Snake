from math import floor
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
                'x':-1,
                'y':0
            },
            3:{
                'direction':(1,0),
                'x':-2,
                'y':0
            },
        }
        self.location = location
        self.root = root

    def getLocation(self,id=None):
        if id:
            return (self.segments.get(self.id).get('x'),self.segments.get(1).get('y'))
        else:
            return (self.segments.get(self.headId).get('x'),self.segments.get(1).get('y'))
    
    def moveSnake(self):
        for idx,item in self.segments.items():
            print(item)
            originalX = item.get('x')
            originalY = item.get('y')
            direction = item.get('direction')
            self.segments.get(idx).update({'x':originalX + direction[0],'y':originalY + direction[1]})
            try:
                prevDirection = self.segments.get(idx-1).get('direction')
            except:
                prevDirection = self.segments.get(idx).get('direction')

            self.segments.get(idx).update({'direction':prevDirection})

def createWindow(cell_size):
    root = tk.Tk()

    root.title("Snake")
    root.configure(background="lightgray")
    root.resizable(False, False)


    for i in range(15):
        for j in range(15):
            e = tk.Frame(root, width=cell_size[0],height=cell_size[1])
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

def showSegement(root,list_of_segments:list[Snake]):
    for seg in list_of_segments:
        cell = getCellFromCords(root,seg.location)
        cell['background'] = 'red'

def checkCollision():
    pass




if __name__=='__main__':

    root = createWindow(CELL_SIZE)

    showGridlines(root)
    # getGridCenter(root)

    snake = Snake(root,(0,0))
    print(snake.getLocation())
    snake.moveSnake()
    snake.moveSnake()

    print(snake.getLocation())

    # root.update()

    # root.mainloop()

