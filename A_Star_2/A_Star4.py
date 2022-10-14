from tkinter import *
from math import sqrt,ceil,log, inf
import string
import datetime
import time
from heapq import heappop, heappush
from tkinter import messagebox
import random

def get_key(val,dictionary): # Return key in dict for given value
    for key, value in dictionary.items(): 
         if val == value: 
             return key 
    return "key doesn't exist"

def distance(start,target): # Return streight path Calculated using Pythagorean theorem
    x_distance = abs(start.coordinate[0] - target.coordinate[0]) 
    y_distance = abs(start.coordinate[1] - target.coordinate[1])
    return sqrt((x_distance**2)+(y_distance)**2)

def get_letters(number): # Return letter coresponding to number (eg.Excel rows)
    alphabet = string.ascii_uppercase
    a_c = len(alphabet) 
    letters = ''
    if number == 1:
        letters += alphabet[0]
    else:
        number_of_letters = ceil(log(number,a_c))
        for i in range(1,number_of_letters+1):
            index_of_letter = number // (a_c**(number_of_letters - i))
            if (number_of_letters - i) >= 1 and (number%(a_c**(number_of_letters - i)))==0:
                letters += alphabet[index_of_letter-2]
            else:
                letters += alphabet[index_of_letter-1]
            num = number % (a_c**(number_of_letters - i))
            number = num
    return(letters)

def getList(dict): # Dict keys to list
    return [*dict]
class Vertex: # Vertex store neighbors, distance from neighbor, coordinates
    def __init__(self,name,x,y):
        self.name = name
        self.coordinate = (x,y)
        self.neighbors = {}
        self.backup = {}
    def __lt__(self, other):
        return self.name < other.name
    def __le__(self, other):
        return self.name <= other.name
    def add_neighbor(self,neighbor):
        self.neighbors[neighbor] = distance(self,neighbor)
    def rem_neighbor(self,neighbor):
        self.backup[neighbor] = self.neighbors[neighbor]
        del self.neighbors[neighbor]
    def get_neighbors(self):
        return(self.neighbors)
    def restore_vertex(self):
        for i in self.backup:
            self.neighbors[i] = self.backup[i]
        self.backup.clear()

class Graph: # Graph store vertexes
    def __init__(self):
        self.graph = []
        self.graph_backup = []
        self.side = 0
    def __len__(self):
        h = len(self.graph)
        return h
    def print_all(self):
        str_graph = ""
        str_graph_backup = ""
        for i in self.graph:
            neigh = ""
            for j in i.neighbors:
                neigh += j.name + " - " + str(i.neighbors[j])
            str_graph += i.name + " " + str(i.coordinate) + " " + neigh +"\n"
        for i in self.graph_backup:
            neigh = ""
            for j in i.neighbors:
                neigh += j.name + " - " + str(i.neighbors[j])
            str_graph_backup += i.name + " " + str(i.coordinate) + " " + neigh + "\n"
        if str_graph_backup == "":
            str_graph_backup = "Backup graph empty."
        if str_graph == "":
            str_graph = "Graph empty."
        print(str_graph)
        print(str_graph_backup)

    def generator(self,a):
        def coord_add(x,y,vert):
            if (x in range(0,a)) and (y in range(0,a)):
                vert.add_neighbor(self.graph[x*a+y])
        start_g = datetime.datetime.now()
        x_a = 0
        y_a = 0
        for i in range(1,(a**2)+1):
            if y_a > (a-1):
                x_a += 1
                y_a = 0
            vertex_letter = get_letters(i)
            vertex_temp = Vertex(vertex_letter,x_a,y_a)
            self.graph.append(vertex_temp)
            y_a += 1
        for i in self.graph:
            x_i = i.coordinate[0]
            y_i = i.coordinate[1]
            # coord_add((x_i - 1),(y_i - 1),i)
            coord_add((x_i - 1),(y_i    ),i)
            # coord_add((x_i - 1),(y_i + 1),i)
            coord_add((x_i    ),(y_i - 1),i)
            coord_add((x_i    ),(y_i + 1),i)
            # coord_add((x_i + 1),(y_i - 1),i)
            coord_add((x_i + 1),(y_i    ),i)
            # coord_add((x_i + 1),(y_i + 1),i)
        end_g = datetime.datetime.now()
        time_delta = end_g - start_g
        print("graph created in : " + str(time_delta))
        self.side = a

    def remove_vertex(self,j):
        nlist = j.get_neighbors()
        for neighbor in nlist:
            neighbor.rem_neighbor(j)
        self.graph_backup.append(j)
        self.graph.remove(j)

    def restore_graph(self):
        for i in self.graph_backup:
            self.graph.append(i)
        self.graph_backup.clear()
        for i in self.graph:
            i.restore_vertex()

class A_Star_Canvas: # Visual representation of graph and A*
    def __init__(self, graph):
        self.top = Toplevel()
        self.top.title("A Start by Turbo")
        self.cells = {}
        self.graph = graph
        self.destinations_letters_dictionary ={}
        for i in graph.graph:
            self.destinations_letters_dictionary[i.name] = i

        graph_len_sqrt = int(sqrt(len(graph)))
        sqr_size = 8
    
        self.canvas1 = Canvas(self.top, width = sqr_size * graph_len_sqrt, height = sqr_size * graph_len_sqrt)
        self.canvas1.grid(row = 0, column = 0,columnspan = 3)
        self.canvas1.bind("<B1-Motion>", self.remove_action)
        self.canvas1.bind("<Button-3>", self.finder)
        for i in graph.graph:
            x = i.coordinate[0]
            y = i.coordinate[1]    
            cell = self.canvas1.create_rectangle(0+sqr_size*x,0+y*sqr_size,sqr_size+sqr_size*x,sqr_size+y*sqr_size,outline="yellow", fill="yellow")
            self.cells[cell] = i

        self.start = Button(self.top, text = "start", width = graph_len_sqrt//2,command = self.a_star_action)
        self.start.grid(row=1, column=1)
        
        self.start = Button(self.top, text = "maze", width = graph_len_sqrt//2,command = self.maze_generator)
        self.start.grid(row=1, column=2)

        self.start_lable = Label(self.top,text = "Starting Point")
        self.start_lable.grid(row=2, column=0)

        self.end_lable = Label(self.top,text = 'End Point')
        self.end_lable.grid(row=3, column=0)

        self.get_start_field = Entry(self.top,width = graph_len_sqrt)
        self.get_start_field.grid(row = 2, column=1)

        self.get_end_field = Entry(self.top,width = graph_len_sqrt)
        self.get_end_field.grid(row=3, column=1)

        self.clear = Button(self.top, text = "clear all", command = self.clear_all)
        self.clear.grid(row=1, column=0)

    def finder(self,event):
        x = self.canvas1.canvasx(event.x)
        y = self.canvas1.canvasy(event.y)
        current = self.canvas1.find_closest(x, y)
        if self.canvas1.itemcget(current,"state") != "disabled":
            if self.get_start_field.get() != '' and self.get_end_field.get() != '':
                self.get_start_field.delete(0,END)
                self.get_end_field.delete(0,END)
            if self.get_start_field.get() == '':
                self.get_start_field.insert(0,self.cells[current[0]].name)
            elif self.get_end_field.get() == '':
                self.get_end_field.insert(0,self.cells[current[0]].name)       
        
    def remove_action(self,event):
        x = self.canvas1.canvasx(event.x)
        y = self.canvas1.canvasy(event.y)
        current = self.canvas1.find_closest(x, y)
        if self.canvas1.itemcget(current,"state") != "disabled":
            self.canvas1.itemconfig(current, fill = "black", outline = "black", state = "disabled")
            self.graph.remove_vertex(self.cells[current[0]])
            # self.graph.print_all()
            # print(len(self.graph))

    def clear_all(self):
        self.graph.restore_graph()
        self.canvas1.itemconfig("all", fill = "yellow", outline = "yellow", state = "normal")
    
    def get_start(self): # user input for start
        start_point_letter = self.get_start_field.get()
        if start_point_letter in self.destinations_letters_dictionary:
            start_point = self.destinations_letters_dictionary[start_point_letter]
            return start_point   
        else:
            self.get_start_field.delete(0, END)

    def get_end(self): # user input for end
        end_point_letter = self.get_end_field.get()
        if end_point_letter in self.destinations_letters_dictionary:
            end_point = self.destinations_letters_dictionary[end_point_letter]
            return end_point   
        else:
            self.get_end_field.delete(0, END)

    def a_star(self,graph,start,target):
        paths_and_distances = {}
        counter = 0
        for vertex in self.graph.graph: # preset paths_and_distances[0] = inf, [1] = inf, [3] = [start] path always begins with start
            paths_and_distances[vertex] = [inf,inf, [start]]
        paths_and_distances[start][1] = 0 # path length at start is 0
        paths_and_distances[start][0] = 0 # heuristic path length at start is 0
        vertices_to_explore = [] #1st vertex to explore
        heappush(vertices_to_explore, (0, 0, start))
        while vertices_to_explore and paths_and_distances[target][0] == inf: # when target is not inf we found our target
            counter += 1
            current_hdistance, current_distance, current_vertex = heappop(vertices_to_explore) # pop from heap vertices_to_explore
            cell_to_update = get_key(current_vertex,self.cells)
            self.canvas1.itemconfig(cell_to_update, fill = "red",outline = "red")
            current_neighbors = current_vertex.get_neighbors()
            for neighbor in current_neighbors:
                new_hdistance = current_hdistance + current_neighbors[neighbor] + distance(neighbor, target)
                new_path = paths_and_distances[current_vertex][2] + [neighbor]
                new_distance = current_distance + current_neighbors[neighbor]
                if new_hdistance < paths_and_distances[neighbor][0]:
                    paths_and_distances[neighbor][0] = new_hdistance
                    paths_and_distances[neighbor][1] = new_distance
                    paths_and_distances[neighbor][2] = new_path
                    heappush(vertices_to_explore, (new_hdistance, new_distance, neighbor)) # push all neighbors to vertices_to_explore heap if they are not inf

        path = ''
        for i in paths_and_distances[target][2]:
            cell_to_update = get_key(i,self.cells)
            self.canvas1.itemconfig(cell_to_update, fill = "green", outline = "green")
            path += ", " + i.name
        messagebox.showinfo("Path Found!", "Found a path in steps {2}. Path length: {1} Path: {0}".format(path,paths_and_distances[target][1],counter))

    def a_star_action(self): # all in one
        a = self.get_start()
        b = self.get_end()
        try:
            self.a_star(self.graph,a,b)
        except KeyError:
            messagebox.showinfo("Error", "Letters not in Graph")
 
class A_Star_Start: # Starter
    def __init__(self, master):
        self.master = master
        master.title("Starter")

        self.entry = Entry()
        self.entry.grid(row = 0 , column = 1)
        self.entry.insert(0, "25")

        self.lable = Label(text = "Graph side size:")
        self.lable.grid(row = 0, column = 0)

        self.generator = Button(text = "Generate Graph", command = self.generate)
        self.generator.grid(row = 1 , column = 0, columnspan = 2)

    def generate(self):
        self.a = int(self.entry.get())
        self.graph_to_gen = Graph()
        self.graph_to_gen.generator(self.a)
        self.window = A_Star_Canvas(self.graph_to_gen)

root = Tk()
my_gui = A_Star_Start(root)
root.mainloop()