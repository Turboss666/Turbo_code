from datetime import datetime
from tkinter import *
import random
import time

# def get_key(val,dictionary): # Return key in dict for given value
#     for key, value in dictionary.items(): 
#          if val == value: 
#              return key 
#     return "key doesn't exist"

#Timer for fuctions
def timer(func):
    def inner1(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print("Total time taken in : ", func.__name__,end - start)
    return(inner1)



class Maze_app:
    def __init__(self,master):
        master.title("Maze generator by Turbo.")
        self.master = master
        self.cells = {}
        sqr_size = 9
        sqr_sides = 80
        a = sqr_sides
        self.good_route = []

        self.canvas1 = Canvas(self.master, width = sqr_size * sqr_sides, height = sqr_size * sqr_sides)
        self.canvas1.pack()
        # self.canvas1.bind("<Button-3>", self.finder)

        self.button_start = Button(text = "start", command = lambda: self.maze_creator(0,0,79,79))
        self.button_start.pack()

        self.show_path_button = Button(text = "show route", command = self.show_route)
        self.show_path_button.pack()

        self.hide_path_button = Button(text = "hide route", command = self.hide_route)
        self.hide_path_button.pack()

        x_a = 0
        y_a = 0
        for i in range(1,(a**2)+1):
            if y_a > (a-1):
                x_a += 1
                y_a = 0
            cell = self.canvas1.create_rectangle(0+sqr_size*x_a, 0+y_a*sqr_size, sqr_size+sqr_size*x_a, sqr_size+y_a*sqr_size, fill="white")
            self.cells[(x_a,y_a)] = cell
            y_a += 1

    def get_neighbors(self,vertex):
        x = vertex[0]
        y = vertex[1]
        neighbors = []
        if (x+1,y) in self.cells.keys():
            neighbors.append((x+1,y))
        if (x,y+1) in self.cells.keys():
            neighbors.append((x,y+1))
        if (x-1,y) in self.cells.keys():
            neighbors.append((x-1,y))
        if (x,y-1) in self.cells.keys():
            neighbors.append((x,y-1))
        return neighbors

    # def get_neighbors_diagonal(self,vertex):
    #     x = vertex[0]
    #     y = vertex[1]
    #     neighbors = []
    #     if (x+1,y) in self.cells.keys():
    #         neighbors.append((x+1,y+1))
    #     if (x,y+1) in self.cells.keys():
    #         neighbors.append((x-1,y+1))
    #     if (x-1,y) in self.cells.keys():
    #         neighbors.append((x-1,y-1))
    #     if (x,y-1) in self.cells.keys():
    #         neighbors.append((x+1,y-1))
    #     return neighbors

    # def finder(self,event):
    #     x = self.canvas1.canvasx(event.x)
    #     y = self.canvas1.canvasy(event.y)
    #     current = self.canvas1.find_closest(x, y)
    #     point = get_key(current[0],self.cells)
    #     if point in self.path:
    #         print(point,"in path!")
    #     else:
    #         print(point,"not in path")   
    @timer
    def maze_creator(self,x,y,x_end,y_end):
        try:
            print("please wait generating maze!")
            self.good_route = []
            wall = []
            path = []
            x_original = x
            y_original = y
            x_end_original = x_end
            y_end_original = y_end
            # self.canvas1.itemconfig(self.cells[(x_original,y_original)], fill = "green")
            # self.canvas1.itemconfig(self.cells[(x_end,y_end)], fill = "green")
            end = (x_end,y_end)
            start = (x,y)
            pointer = (x,y)            
            while pointer != end:
                proper_neighbors = []
                pointer_neighbors = self.get_neighbors(pointer)
                for i in pointer_neighbors:
                    if (i not in wall) and (i not in path):
                        proper_neighbors.append(i)
                if proper_neighbors != []:
                    if end in proper_neighbors:
                        rando = end
                    else:
                        rando = random.choice(proper_neighbors)
                    path.append(rando)
                    for i in pointer_neighbors:
                        if (i not in wall) and (i not in path):
                            wall.append(i)
                            # self.canvas1.itemconfig(self.cells[i], fill = "black")
                    cell_to_update = self.cells[rando]
                    # self.canvas1.itemconfig(cell_to_update, fill = "red")
                    pointer = rando
                else:
                    backtrack = 3
                    pointer = path[-backtrack]
                    pointer_neighbors = self.get_neighbors(pointer)
                    # self.canvas1.itemconfig(self.cells[pointer], fill = "orange")
                    for i in pointer_neighbors:
                        i_neighbors = self.get_neighbors(i)
                        if (i in wall) and (i_neighbors not in path):
                            wall.remove(i)
                            # self.canvas1.itemconfig(self.cells[i], fill = "yellow")
                    for i in path[-(backtrack-1):]:
                        wall.append(i)
                        # self.canvas1.itemconfig(self.cells[i], fill = "green")
                    path = path[0:-backtrack]
                    path.append(pointer)
                    # user_input = input("Press any key to continue!")
                    # for i in wall:
                        # self.canvas1.itemconfig(self.cells[i], fill = "black")
            # user_input = input("Random path found! press any key to continue")
            # for i in self.cells:
                # if self.canvas1.itemcget(self.cells[i],"fill") == "black":
                    # self.canvas1.itemconfig(self.cells[i], fill = "white")
            wall = []
            for i in path:
                i_neighbors = self.get_neighbors(i)
                for j in i_neighbors:
                    if j not in path:
                        # self.canvas1.itemconfig(self.cells[j], fill = "black")
                        wall.append(j)
                self.good_route.append(i)
                # self.canvas1.itemconfig(self.cells[i], fill = "green")
            # user_input = input("Removed excessive wall! press any key to continue")
        except IndexError:
            wall = []
            path = []
            self.good_route = []
            self.maze_creator(x,y,x_end,y_end)
        def maze_branching(count):
            for i in range(count): 
                available_start_points = []
                for i in path:
                    i_neighbors = self.get_neighbors(i)
                    for j in i_neighbors:
                        j_neighbors = self.get_neighbors(j)
                        for k in j_neighbors:
                            if k not in wall and k not in path:
                                available_start_points.append(j)
                                break
                # user_input = input("All anavailable crossroads - Green! press any key to continue")
                proper_start_points = []
                for i in available_start_points:
                    i_neighbors = self.get_neighbors(i)
                    collisions_with_start_points = 0
                    collisions_with_path = 0
                    collisions_with_self = 0
                    for j in i_neighbors:
                        if j in available_start_points:
                            collisions_with_start_points += 1
                        if j in path:
                            collisions_with_path += 1
                        if j in proper_start_points:
                            collisions_with_self += 1
                    if collisions_with_start_points == 0 and collisions_with_path <= 1:
                        proper_start_points.append(i)
                        # self.canvas1.itemconfig(self.cells[i], fill = "yellow")
                    if collisions_with_start_points == 2 and collisions_with_path <= 1 and collisions_with_self == 0:
                        proper_start_points.append(i)
                        # self.canvas1.itemconfig(self.cells[i], fill = "yellow")
                # user_input = input("All proper crossroads - Yellow! press any key to continue")
                
                for i in proper_start_points:
                    wall.remove(i)
                for i in proper_start_points:
                    # user_input = input("press any key to continue")
                    pointer = i
                    if pointer not in wall:
                        path.append(pointer)
                    # self.canvas1.itemconfig(self.cells[pointer], fill = "red")
                    while pointer not in wall:
                        proper_neighbors = []
                        pointer_neighbors = self.get_neighbors(pointer)                        
                        for i in pointer_neighbors:
                            if (i not in wall) and (i not in path) and (i not in proper_start_points):
                                proper_neighbors.append(i)
                        if proper_neighbors != []:
                            rando = random.choice(proper_neighbors)
                            path.append(rando)
                            for i in pointer_neighbors:
                                if (i not in wall) and (i not in path):
                                    wall.append(i)
                                    # self.canvas1.itemconfig(self.cells[i], fill = "black")
                            # cell_to_update = self.cells[rando]
                            # self.canvas1.itemconfig(cell_to_update, fill = "red")
                            pointer = rando
                        else:
                            for i in pointer_neighbors:
                                if (i not in wall) and (i not in path):
                                    wall.append(i)
                                    # self.canvas1.itemconfig(self.cells[i], fill = "black")
                            path.remove(pointer)
                            wall.append(pointer)
                            break

        maze_branching(4)
        for i in self.cells:
            self.canvas1.itemconfig(self.cells[i], fill = "white")

        for i in path:
            self.canvas1.itemconfig(self.cells[i], fill = "red")

        for i in wall:
            self.canvas1.itemconfig(self.cells[i], fill = "black")

        self.canvas1.itemconfig(self.cells[start], fill = "green")
        self.canvas1.itemconfig(self.cells[end], fill = "green")
        for i in self.cells:
            if self.canvas1.itemcget(self.cells[i],"fill") == "white":
                self.canvas1.itemconfig(self.cells[i], fill = "black")


        

    def show_route(self):
        for i in self.good_route:
            self.canvas1.itemconfig(self.cells[i], fill = "green")
    def hide_route(self):
        for i in self.good_route:
            self.canvas1.itemconfig(self.cells[i], fill = "red")




root = Tk()
my_gui = Maze_app(root)
root.mainloop()
