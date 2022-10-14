from math import sqrt,ceil,log, inf
import string
import datetime
import time
from heapq import heappop, heappush
from tkinter import *
from tkinter import messagebox

def distance(start,target): # Calculate straight distance using Pythagorean theorem
    x_distance = abs(start.coordinate[0] - target.coordinate[0]) 
    y_distance = abs(start.coordinate[1] - target.coordinate[1])
    return sqrt((x_distance**2)+(y_distance)**2)

def get_letters(number):
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

class vertex:
    def __init__(self,name,x,y):
        self.name = name
        self.coordinate = (x,y)
        self.neighbors = {}
    def __lt__(self, other):
        return self.name < other.name
    def __le__(self, other):
        return self.name <= other.name
    def add_neighbor(self,neighbor):
        self.neighbors[neighbor] = distance(self,neighbor)
    def rem_neighbor(self,neighbor):
        del self.neighbors[neighbor]
    def get_neighbors(self):
        return(self.neighbors)

def graph_generator(a):
    def coord_add(x,y,vert):
        if (x in range(0,a)) and (y in range(0,a)):
            vert.add_neighbor(graph[x*a+y])
    
    start_g = datetime.datetime.now()
    graph = []
    x_a = 0
    y_a = 0
    for i in range(1,(a**2)+1):
        if y_a > (a-1):
            x_a += 1
            y_a = 0
        vertex_letter = get_letters(i)
        vertex_temp = vertex(vertex_letter,x_a,y_a)
        graph.append(vertex_temp)
        y_a += 1
    for i in graph:
        x_i = i.coordinate[0]
        y_i = i.coordinate[1]
        coord_add((x_i - 1),(y_i - 1),i)
        coord_add((x_i - 1),(y_i    ),i)
        coord_add((x_i - 1),(y_i + 1),i)
        coord_add((x_i    ),(y_i - 1),i)
        coord_add((x_i    ),(y_i + 1),i)
        coord_add((x_i + 1),(y_i - 1),i)
        coord_add((x_i + 1),(y_i    ),i)
        coord_add((x_i + 1),(y_i + 1),i)
    end_g = datetime.datetime.now()
    time_delta = end_g - start_g
    print("graph created in : " + str(time_delta))
    return graph
    
def a_star(graph,start,target):
    paths_and_distances = {}
    counter = 0
    for vertex in graph: # preset paths_and_distances[0] = inf [1] = inf [3] = [start.name] path always begins with start
        paths_and_distances[vertex] = [inf,inf, [start]]
    paths_and_distances[start][1] = 0 # path length at start is 0
    paths_and_distances[start][0] = 0 # heuristic path length at start is 0
    vertices_to_explore = [] #1st vertex to explore
    heappush(vertices_to_explore, (0, 0, start))
    while vertices_to_explore and paths_and_distances[target][0] == inf: # when target is not inf we found our target
        counter += 1
        current_hdistance, current_distance, current_vertex = heappop(vertices_to_explore) # pop from heap vertices_to_explore
        cells[(current_vertex.coordinate[0],current_vertex.coordinate[1])].configure(background = 'red')
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
                # print("\nmatch At " + vertices_to_explore[0][1].name)
        #testing
    path = ''
    for i in paths_and_distances[target][2]:
        cells[(i.coordinate[0],i.coordinate[1])].configure(background = 'green')
        path += ", " + i.name
    # print("Found a path in steps {2}. Path length: {1} Path: {0}".format(path,paths_and_distances[target][1])
    messagebox.showinfo("Path Found!", "Found a path in steps {2}. Path length: {1} Path: {0}".format(path,paths_and_distances[target][1],counter))

def get_start(): # user input for start
  start_point_letter = ""
  if start_point_letter not in destinations_letters:
      start_point_letter = cells["get_start_field"].get()
    #   start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
      if start_point_letter in destinations_letters:
        start_point = destinations_letters_dictionaty[start_point_letter]
        return start_point   
      else:
        cells["get_start_field"].delete(0, END)

def get_end(): # user input for end
    end_point_letter = ""
    if end_point_letter not in destinations_letters:
      end_point_letter = cells["get_end_field"].get()
    #   end_point_letter = input("Ok, where are you headed? Type in the corresponding letter: ")
      if end_point_letter in destinations_letters:
        end_point = destinations_letters_dictionaty[end_point_letter]
        return end_point   
      else:
        cells["get_end_field"].delete(0, END)

def show_destination(): # show map of destination and letter linking them for user input
    for k,v in destinations_letters_dictionaty.items():
        print("{} - {}".format(k,v.name))

def greet(): # all in one
    a = get_start()
    b = get_end()
    try:
        a_star(gtc,a,b)
    except KeyError:
        messagebox.showinfo("Error", "Letters not in Graph")
    
def click_remove_vertex(j,graph):
    nlist = j.get_neighbors()
    for neighbor in nlist:
        neighbor.rem_neighbor(j)
    graph.remove(j)
    cells[(j.coordinate[0],j.coordinate[1])].configure(state = DISABLED,bg = 'black')
    print(j.name," Removed.")

def grid_builder(graph):
    graph_len_sqrt = int(sqrt(len(graph)))
    cells = {}
    for i in graph:
        row = i.coordinate[0]
        column = i.coordinate[1]    
        cell = Button(root, text = i.name, bg='white',height = 1, width =2,command = lambda i = i:click_remove_vertex(i,graph)) #,command = lambda i = i:click_remove_vertex(i,graph)
        cell.grid(row=row, column=column)
        # cell.bind('<Enter>',lambda event, i = i: click_remove_vertex(i,graph))
        cells[(row, column)] = cell 
    start = Button(root, text = "start", command = lambda: greet(), width = graph_len_sqrt)
    start.grid(row=graph_len_sqrt +1, column=0,columnspan = graph_len_sqrt//2)
    start_lable = Label(root,text = "Starting Point")
    start_lable.grid(row=graph_len_sqrt +2, column=0,columnspan = graph_len_sqrt//2)
    end_lable = Label(root,text = 'End Point')
    end_lable.grid(row=graph_len_sqrt +3, column=0,columnspan = graph_len_sqrt//2)
    get_start_field = Entry(root)
    get_start_field.grid(row=graph_len_sqrt +2, column=graph_len_sqrt//2,columnspan = graph_len_sqrt//2)
    get_end_field = Entry(root)
    get_end_field.grid(row=graph_len_sqrt +3, column=graph_len_sqrt//2,columnspan = graph_len_sqrt//2)
    clear = Button(root, text = "clear all", command = lambda: clear_all(gtc,backup_graph))
    clear.grid(row=graph_len_sqrt +1, column= graph_len_sqrt//2,columnspan = graph_len_sqrt//2)
    cells["start"] = start
    cells["start_lable"] = start_lable
    cells["end_lable"] = end_lable
    cells["get_start_field"] = get_start_field
    cells["get_end_field"] = get_end_field
    cells["clear"] = clear
    return cells

def clear_all(graph,backup_graph):
    for i in cells:
        if i is tuple:
            cells[i].configure(background = 'gray')
    graph = backup_graph
    print("hi")
    return graph

root = Tk()
alphabet = string.ascii_uppercase
a_c = len(alphabet)
gtc = graph_generator(20)
backup_graph = gtc
destinations = [a for a in gtc] # List of all vertices
destinations_letters = [a.name for a in destinations] # List of all 1st letters in destination
i = 0 # pointer for dict creation
destinations_letters_dictionaty = {} # Dict linking destination with it's 1st letter for easy user input
for letter in destinations_letters:
    destinations_letters_dictionaty[letter] = destinations[i]
    i += 1
cells = grid_builder(gtc)
root.mainloop()