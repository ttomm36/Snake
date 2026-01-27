from math import floor
import time
import tkinter as tk

CELL_SIZE = 50,50

class Snake:
    def __init__(self,root,id,location):
        self.id = id
        self.location = location
        self.root = root

    def getLocation(self):
        return self.location
    
    def setLocation(self,loc):
        self.location = loc

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

def updateSegmentsLocation(direction,list_of_segments:list[Snake]):
    updated_list_of_segments = []
    for seg in list_of_segments:
        if seg.id == 0:
            current_location = seg.getLocation()
            match direction:
                case 'd':
                    new_y = current_location[0] - 1
                    new_x = current_location[1]
                case 'u':
                    new_y = current_location[0] + 1
                    new_x = current_location[1]
                case 'l':
                    new_y = current_location[0] 
                    new_x = current_location[1] -1
                case 'r':
                    new_y = current_location[0] 
                    new_x = current_location[1] + 1
            seg.setLocation((new_x,new_y))
        updated_list_of_segments.append(seg)
    return updated_list_of_segments
def checkCollision():
    pass




if __name__=='__main__':

    root = createWindow(CELL_SIZE)

    showGridlines(root)
    # getGridCenter(root)

    seg = Snake(root,0,(0,0))
    x = [seg]

    showSegement(root,x)
    root.update()

    time.sleep(10)

    x = updateSegmentsLocation('u',x)

    showSegement(root,x)
    root.update()

    root.mainloop()

